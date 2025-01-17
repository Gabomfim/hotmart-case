from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from transformers import pipeline
import os

# Initialize ChromaDB client
vector_db = chromadb.HttpClient(host='http://vector-db:8000')

# Retrieve the existing collection
collection_name = 'html_embeddings'
collection = vector_db.get_or_create_collection(collection_name)

# Load Hugging Face's LLM pipeline
# You can use a lightweight model like GPT-Neo for faster inference
llm = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B', device=-1)

# FastAPI app configuration
app = FastAPI()

# Input models
class QueryInput(BaseModel):
    """
    Input model for the /query endpoint.
    Represents a semantic search query.
    """
    query: str


@app.get('/')
def health_check():
    """
    Health check endpoint for the QueryAPI.

    Returns:
        dict: A dictionary containing the status of the service.
    """
    return {'status': 'running'}


@app.post('/query')
def query_with_llm(input_data: QueryInput):
    """
    Performs a semantic search and generates a response using an open-source LLM.

    Args:
        input_data (QueryInput): The input question for the semantic search and LLM.

    Returns:
        dict: A dictionary containing:
            - A success message.
            - The generated response from the LLM.
            - The context retrieved from the vector database.
    """
    try:
        # Step 1: Query the vector database
        results = collection.query(
            query_texts=[input_data.query],
            n_results=3  # Return top 5 results
        )

        # Step 2: Format the context from the vector database
        context = '\n'.join(
            metadata['content']
            for metadatas_list in results['metadatas']
            for metadata in metadatas_list
        )

        if not context.strip():
            raise ValueError('No relevant context found in the vector database.')

        # Step 3: Use the open-source LLM to generate a response
        prompt = (
            f"Você é um assistente especializado em responder perguntas com base no contexto fornecido.\n\n"
            f"Contexto:\n{context}\n\n"
            f"Pergunta: {input_data.query}\n\n"
            f"Resposta:"
        )

        llm_response = llm(
            prompt,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            num_return_sequences=1
        )[0]['generated_text']

        return {
            'message': 'Query and response generated successfully',
            'query': input_data.query,
            'context': context,
            'response': llm_response
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal error: {e}') from e
