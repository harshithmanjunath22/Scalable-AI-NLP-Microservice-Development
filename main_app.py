import ray
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from transformers import pipeline
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv() # Access the environment variables 

username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

encoded_username = quote_plus(username)  # RFC Standard
encoded_password = quote_plus(password)

# Initialize FastAPI app and MongoDB client
app = FastAPI()
mongo_client = MongoClient(
    f"mongodb://{encoded_username}:{encoded_password}@localhost:27017/"
)
db = mongo_client["myDatabase"]
articles_collection = db["articles"]

# Ray initialization
ray.init()


# Pydantic model for article data
class Article(BaseModel):
    uri: str
    title: str
    body: str


# Max input length for each chunk
MAX_CHUNK_SIZE = 800  # Token count for each chunk

# Number of replicas (configurable)
num_replicas = 2


# Define Ray actor for summarization
@ray.remote
class SummarizerActor:
    def __init__(self):
        # Initialize the summarizer model inside the actor
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text_chunk: str):
        try:
            # Perform text summarization with adjusted length parameters
            summary = self.summarizer(
                text_chunk, max_length=150, min_length=50, do_sample=False
            )[0]["summary_text"]
            return summary
        except IndexError:
            # Handle issues with input length
            raise ValueError(
                "The summarization process encountered an issue with the input length."
            )


# Create multiple replicas of the SummarizerActor
summarizer_actors = [SummarizerActor.remote() for _ in range(num_replicas)]


# Function to handle round-robin selection
def get_next_actor():
    current_actor = 0
    while True:
        yield summarizer_actors[current_actor]
        current_actor = (current_actor + 1) % num_replicas


# Round-robin generator
actor_generator = get_next_actor()


def chunk_text(text: str, chunk_size: int):
    # Split text into words
    words = text.split()
    # Create chunks of text with the specified size
    return [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]


@app.post("/summarize_article")
async def summarize_article(article: Article):
    # Split the input body into manageable chunks
    chunks = chunk_text(article.body, MAX_CHUNK_SIZE)

    # Use round-robin to distribute summarization tasks among replicas
    summary_futures = [
        next(actor_generator).summarize.remote(chunk) for chunk in chunks
    ]

    # Use ray.get to fetch results from Ray's ObjectRefs
    summary_chunks = ray.get(summary_futures)

    # Combine all the summary chunks into one summary
    combined_summary = " ".join(summary_chunks)

    # Store article and summary in MongoDB
    articles_collection.insert_one(
        {
            "uri": article.uri,
            "title": article.title,
            "body": article.body,
            "summary": combined_summary,
        }
    )
    return {"uri": article.uri, "summary": combined_summary}


@app.get("/result/{uri}")
async def get_summary(uri: str):
    # Retrieve the summarized article from MongoDB
    article = articles_collection.find_one({"uri": uri})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {
        "uri": article["uri"],
        "title": article["title"],
        "summary": article["summary"],
    }
