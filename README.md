# **Hotmart Case**

This project provides two microservices, **HTML2VectorAPI** and **QueryAPI**, enabling semantic text processing, storage, and retrieval with enhanced LLM-powered contextual responses. It leverages a vector database (**ChromaDB**) to store semantic embeddings and uses an open-source LLM (**GPT-Neo 1.3B**) for generating responses based on retrieved context.

## **Table of Contents**

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Known Issues](#known-issues)
- [Future Enhancements](#future-enhancements)

## **Overview**

This project demonstrates the ability to:
- Extract meaningful text content from HTML documents via the **HTML2VectorAPI**.
- Generate and store semantic embeddings in a vector database.
- Perform semantic searches and use an **LLM** to generate contextual answers via the **QueryAPI**.

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
   - Uses the retrieved context to generate human-like responses with **GPT-Neo 1.3B**.

## **Features**

- **Text Processing**:
   - Removes unnecessary tags (e.g., `<script>`, `<style>`).
   - Cleans and filters paragraphs to ensure quality embeddings.

- **Semantic Embeddings**:
   - Generates embeddings using **Sentence Transformers**.
   - Stores embeddings in a vector database for efficient search and retrieval.

- **LLM Integration**:
   - Uses the **GPT-Neo 1.3B** model to provide detailed, human-like answers based on retrieved context.
   - Supports custom prompts and controlled text generation.

- **Semantic Search**:
   - Retrieves the most relevant context for a query.
   - Combines results into a coherent input for the LLM.

## **Setup Instructions**

### Prerequisites

- Docker and Docker Compose installed.
- Python 3.10+ (for local development).
- At least 16GB VRAM for the LLM component, or use CPU with reduced performance.

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

#### Query with LLM
- **URL**: `POST /query`
- **Input**:
  ```json
  {"query": "Como ser um afiliado?"}
  ```
- **Response**:
  ```json
  {
      "message": "Query and response generated successfully",
      "query": "Como ser um afiliado?",
      "context": "Relevant content 1\nRelevant content 2",
      "response": "To become an affiliate, you need to..."
  }
  ```

## **Testing**

To test the services:

1. **Health Checks**:
   ```bash
   curl http://localhost:8001/
   curl http://localhost:8002/
   ```

2. **Process URL**:
   ```bash
   curl -X POST http://localhost:8001/process-url \
        -H "Content-Type: application/json" \
        -d '{"url": "https://hotmart.com/pt-br/blog/como-funciona-hotmart"}'
   ```

3. **Query with LLM**:
   ```bash
   curl -X POST http://localhost:8002/query \
        -H "Content-Type: application/json" \
        -d '{"query": "Como ser um afiliado?"}'
   ```

## **Technologies Used**

- **FastAPI**: Framework for building APIs.
- **ChromaDB**: Vector database for semantic embeddings.
- **Sentence Transformers**: Library for generating semantic embeddings.
- **Hugging Face Transformers**: For LLM-based text generation.
- **Docker & Docker Compose**: For containerization and orchestration.

## **Known Issues**

- The chosen LLM(`EleutherAI/gpt-neo-1.3B`) is prone to hallucinating, but since the processing power is limited, it was chosen to perform faster inferences.
- Context needs to be better extracted by joining paragraphs, headers and lists.
- The API takes a significant time to respond, so be pacient.

## **Future Enhancements**

- **Fine-Tune LLM**:
   - Customize the LLM for specific use cases to improve relevance and accuracy.

- **Deployment**:
   - Deploy the service in production environment with a better model.

- **Authentication**:
   - Add API key-based authentication for secure access.

- **Dynamic Context Size**:
   - Allow users to specify the number of results or tokens for the response.

- **Enhanced Monitoring**:
   - Integrate logging and monitoring tools.
