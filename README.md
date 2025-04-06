### Scalable AI/NLP Microservice Development

#### Context:
As the landscape of AI and Natural Language Processing (NLP) evolves, the ability to deploy scalable, efficient, and robust microservices has become critical for modern applications. This task is designed to evaluate your proficiency in developing such services using Python and key technologies like FastAPI, MongoDB, Ray, and Hugging Face Transformers. Your challenge is to build a microservice that can summarize articles and handle high volumes of requests efficiently.


#### Task Overview:
You are required to develop a microservice with two RESTful API endpoints using FastAPI. The service will focus on summarizing articles and storing them in a MongoDB database. You will also implement replication and concurrency features to ensure the service can handle multiple requests efficiently. A sample data list of aricles will be provided to you to test your summay endpoint.

### **Steps to Complete the Task:**

1. **Environment Setup:**
   - Set up a Python development environment.
   - Install necessary libraries including `FastAPI`, `MongoDB` python client, `Ray`, and `transformers`.
   - Configure MongoDB, see below, ensuring that you can connect to it from your service.

2. **API Development - Article Summarization Endpoint:**
   - **Create a POST `/summarize_article` Endpoint:**
     - Design and implement an endpoint that accepts an article in the form of JSON, summarizing the article's body using a pre-trained model from Hugging Face's Transformers library.
     - The Huggingface transformer model can be any simple model that is fit into a 16Gi RAM of a normal Laptop.
     - Store the original article and its summary in a MongoDB collection named `articles`.
   
   - **Create a GET `/result` Endpoint:**
     - Implement a retrieval endpoint that fetches the summarized article from MongoDB based on the provided `uri`.

3. **Concurrency and Replication:**
   - **Handle Multiple Concurrent Requests:**
     - Design the POST endpoint to handle multiple requests asynchronously, ensuring that your microservice remains responsive under load.
     - Implement concurrency using asynchronous programming in Python.
   
   - **Implement Replication:**
     - Use Ray to enable your service to replicate and manage high volumes of requests. The number of replicas should be configurable, with a default of 2.

4. **Data Validation:**
   - Implement Pydantic models for validating incoming request data.
   - Ensure robust type hints and comments in your code.

5. **Testing and Optimization:**
   - [Bonus] Write unit tests to validate the core functionality of your endpoints.
   - Optimize your microservice for performance, focusing on efficient request handling and response times.

6. **Containerization (Bonus):**
   - Create a Dockerfile and Docker Compose configuration to containerize your microservice, making it easy to deploy and run.

7. **Documentation:**
   - Write a comprehensive `Readme.md` file, explaining how to set up, run, and use your microservice.
   - Include examples of API requests and responses, as well as any configuration options for replication and concurrency.


## MongoDB Setup with Docker Compose

This guide will help you set up a MongoDB instance using Docker Compose.

### Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

### Setup instrunction
Setup your environment:
```bash
export $(grep -v '^#' .env| xargs)
```
Run docker compose to spin up the mongo
```bash
docker compose up -d
```
Verify you have access to the database and collection:
```bash
docker exec -it mongodb mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin
use myDatabase
show collections
```
you should see `articles` in the output as the result. If not, you can manually create it.
