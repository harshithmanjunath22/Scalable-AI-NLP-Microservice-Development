
# Scalable AI/NLP Microservice Development

## Overview
This microservice leverages `FastAPI`, `Ray`, `Hugging Face Transformers`, and `MongoDB` to provide a scalable solution for summarizing articles. The service handles concurrent requests efficiently and stores both the original article and its summary in MongoDB for retrieval.

## Table of Contents
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Configuration](#configuration)
- [Replication and Concurrency](#replication-and-concurrency)
- [Conclusion](#conclusion)

## Setup and Installation

### Prerequisites
- **Python 3.8+**
- **Docker & Docker Compose** (for containerization)
- **MongoDB**

### Environment Setup

1. **Clone the Repository**

   ```bash
   git clone nlp-microservice-zltiyz (clone this repository)
   cd nlp-microservice-zltiyz
   ```

2. **Install Dependencies**

   Create a virtual environment and activate it:

   ```bash
   python3 -m venv nlp_env
   source env/bin/activate
   ```

   Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   Start the FastAPI app:

   ```bash
   uvicorn main_app:app --host 0.0.0.0 --port 8000
   ```

   The server will be available at `http://localhost:8000`.

## Usage

### Endpoints

1. **POST `/summarize_article`**
   - Summarizes the body of an article.
   - **Request Body:**
     ```json
     {
       "uri": "sample-uri",
       "title": "Sample Title",
       "body": "This is the article content that needs to be summarized."
     }
     ```
   - **Response:**
     ```json
     {
       "uri": "sample-uri",
       "summary": "This is the summarized content."
     }
     ```

2. **GET `/result/{uri}`**
   - Retrieves the summarized article based on the `uri`.
   - **Response:**
     ```json
     {
       "uri": "sample-uri",
       "title": "Sample Title",
       "summary": "This is the summarized content."
     }
     ```

### Sample Requests

- **Summarize an Article**
  ```bash
  curl -X POST "http://localhost:8000/summarize_article" -H "Content-Type: application/json" -d '{
      "uri": "article-1",
      "title": "Sample Article",
      "body": "This is the body of the article to be summarized."
  }'
  ```

- **Retrieve a Summary**
  ```bash
  curl -X GET "http://localhost:8000/result/article-1"
  ```

## Testing

1. **Run Unit Tests**

   To run the tests, make sure you have added test cases for both endpoints under the `tests/` directory.

   ```bash
   pytest tests/
   ```

## Docker Deployment

### Create `Dockerfile`

```dockerfile
FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    environment:
      MONGO_INITDB_ROOT_USERNAME: myUser
      MONGO_INITDB_ROOT_PASSWORD: myP@ssw0rd
    ports:
      - "27017:27017"
```

### Build and Run the Service

```bash
docker-compose up --build
```

## Configuration

- **Replication**: Configure the number of Ray actor replicas by setting the `num_replicas` variable in `main_app.py`.
- **MongoDB Connection**: The MongoDB connection string uses encoded credentials for safety.

## Replication and Concurrency

- The microservice uses `Ray` to manage concurrent summarization tasks.
- The `SummarizerActor` is replicated based on the `num_replicas` variable to balance the load among multiple actors.

## Conclusion

This microservice efficiently summarizes articles, stores the data in MongoDB, and is capable of handling high-concurrency scenarios with Ray. It can be containerized using Docker for easy deployment.

