# **Hotmart Case**

## **Description**:
This project consists of two microservices designed to process and manage textual data, enabling the generation of embeddings for texts in HTML documents and the ability to query stored knowledge efficiently. The solution is optimized for use cases such as semantic search, contextualized question answering, and knowledge-based applications.

---

## **Microservices**:

### **1. HTML2VectorAPI**:
- **Purpose**: 
  Processes HTML documents by extracting meaningful textual content, generating embeddings, and storing them in a vector database.
- **Features**:
  - Accepts URLs of HTML documents.
  - Cleans unnecessary tags (e.g., `<script>`, `<style>`).
  - Splits text into meaningful paragraphs.
  - Generates embeddings using machine learning models (e.g., SentenceTransformers).
  - Saves embeddings and metadata in an open-source vector database like ChromaDB.
- **Use case**:
  Building a knowledge base for efficient retrieval of contextual information.

---

### **2. QueryAPI**:
- **Purpose**:
  Provides an interface for querying the stored knowledge base and retrieving contextually relevant answers.
- **Features**:
  - Accepts a question in natural language as input.
  - Converts the question into an embedding.
  - Queries the vector database to find the most relevant information.
  - Optionally, integrates with a language model (e.g., GPT) to generate a detailed response based on the retrieved context.
- **Use case**:
  Enabling semantic search or answering questions based on stored knowledge.

---

## **Architecture**:
1. **Vector Database**:
   - A shared vector database (e.g., ChromaDB) stores embeddings and metadata.
   - Both microservices interact with the database: one for writing (HTML2VectorAPI) and the other for querying (QueryAPI).
2. **Dockerized Deployment**:
   - Each microservice is containerized with Docker.
   - Deployment is managed using Docker Compose and AWS Elastic Beanstalk.
3. **Scalability**:
   - Designed to scale horizontally with multiple instances of each microservice running behind a load balancer.

---

## **Technologies Used**:
- **Backend**:
  - FastAPI: Lightweight framework for building APIs.
  - SentenceTransformers: For generating embeddings from textual data.
- **Database**:
  - ChromaDB: Open-source vector database for efficient similarity searches.
- **Deployment**:
  - Docker and Docker Compose.
  - AWS Elastic Beanstalk for cloud deployment.

---

## **Workflow**:
1. A user sends an HTML document URL to **HTML2VectorAPI**.
2. The microservice extracts the text, generates embeddings, and stores them in the vector database.
3. Another user submits a question to **QueryAPI**.
4. QueryAPI retrieves relevant context from the vector database and optionally uses a language model to provide a comprehensive response.

---

## **Use Cases**:
- Knowledge-based applications (e.g., FAQs, documentation search).
- Semantic search for specific domains.
- Contextualized question-answering systems.