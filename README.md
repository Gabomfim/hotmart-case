# **Hotmart Case**

This project provides two microservices, **HTML2VectorAPI** and **QueryAPI**, to enable semantic text processing and search functionality using a vector database (powered by ChromaDB). The APIs allow users to process HTML content, store semantic embeddings, and perform semantic queries to retrieve relevant results.

## **Table of Contents**

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)


## **Overview**

This project demonstrates the ability to:
- Extract meaningful text content from HTML documents.
- Generate and store semantic embeddings in a vector database.
- Perform semantic searches using the stored embeddings to retrieve the most relevant results.

## **Architecture**

The system consists of three main components:

1. **Vector Database (`vector-db`)**:
   - Powered by **ChromaDB**.
   - Stores semantic embeddings of processed text.

2. **HTML2VectorAPI (`html2vector`)**:
   - Processes HTML content from a given URL.
   - Extracts and cleans text.
   - Generates embeddings and stores them in the vector database.

3. **QueryAPI (`queryapi`)**:
   - Performs semantic searches on the vector database.
   - Returns the most relevant results with metadata and similarity scores.

## **Features**

- **Text Processing**:
  - Removes unnecessary tags (e.g., `<script>`, `<style>`).
  - Filters out short or irrelevant text blocks.
  - Merges inline elements (e.g., `<span>`, `<b>`) into parent blocks for consistency.

- **Semantic Embeddings**:
  - Generates embeddings using **Sentence Transformers**.
  - Stores embeddings in a vector database for efficient search and retrieval.

- **Semantic Search**:
  - Allows users to query stored embeddings to retrieve the most relevant text results.

## **Setup Instructions**

### Prerequisites

- Docker and Docker Compose installed.
- Python 3.10+ (for local development).
- Basic knowledge of FastAPI and Docker.

### Steps

1. Clone the repository:
   ```bash
   git clone git@github.com:Gabomfim/hotmart-case.git
   cd hotmart-case
   ```

2. Build and start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - **HTML2VectorAPI**: `http://localhost:8001`
   - **QueryAPI**: `http://localhost:8002`

## **API Endpoints**

### **HTML2VectorAPI**

#### Health Check
- **URL**: `GET /`
- **Response**:
  ```json
  {"status": "running"}
  ```

#### Process URL
- **URL**: `POST /process-url`
- **Input**:
  ```json
  {"url": "https://example.com"}
  ```
- **Response**:
  ```json
  {
      "message": "URL processed successfully!",
      "num_paragraphs": 5,
      "paragraphs": [
          "Paragraph 1 text...",
          "Paragraph 2 text...",
          "...and so on."
      ]
  }
  ```

### **QueryAPI**

#### Health Check
- **URL**: `GET /`
- **Response**:
  ```json
  {"status": "running"}
  ```

#### Query
- **URL**: `POST /query`
- **Input**:
  ```json
  {"query": "example search text"}
  ```
- **Response**:
  ```json
  {
      "message": "Query executed successfully",
      "results": [
          {"content": "Relevant text 1", "score": 0.95},
          {"content": "Relevant text 2", "score": 0.90}
      ]
  }
  ```

## **Testing**

To test the services:

1. **Health Check:**
   ```bash
   curl http://localhost:8001/
   curl http://localhost:8002/
   ```

2. **Process URL:**
   ```bash
   curl -X POST http://localhost:8001/process-url \
        -H "Content-Type: application/json" \
        -d '{"url": "https://example.com"}'
   ```

3. **Query:**
   ```bash
   curl -X POST http://localhost:8002/query \
        -H "Content-Type: application/json" \
        -d '{"query": "example search text"}'
   ```

## **Technologies Used**

- **FastAPI**: Framework for building APIs.
- **ChromaDB**: Vector database for semantic embeddings.
- **Sentence Transformers**: Library for generating semantic embeddings.
- **BeautifulSoup**: Library for parsing and cleaning HTML.
- **Docker & Docker Compose**: For containerization and orchestration.

## **Future Enhancements**

- **Authentication**:
  - Add API key-based authentication for secure access.

- **Deployment**:
  - Deploy the service in production environment.

- **Configurable Parameters**:
  - Allow users to specify the number of results returned or the minimum paragraph length dynamically.

- **Additional Integrations**:
  - Support other embedding models or databases.

- **Error Monitoring**:
  - Implement logging and monitoring tools.
