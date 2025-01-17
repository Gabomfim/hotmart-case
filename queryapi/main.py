from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings


# Initialize ChromaDB client
vector_db = chromadb.HttpClient(host='http://vector-db:8000')

# Retrieve the existing collection
collection_name = 'html_embeddings'
collection = vector_db.get_or_create_collection(collection_name)

# FastAPI app configuration
app = FastAPI()


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
def query_vector_database(input_data: QueryInput):
    """
    Performs a semantic search on the vector database and retrieves the most relevant results.

    Args:
        input_data (QueryInput): The input query string for semantic search.

    Returns:
        dict: A dictionary containing:
            - A success message.
            - A list of the top results with their metadata and relevance scores.

    Raises:
        HTTPException: If a ValueError or unexpected error occurs during processing.
    """
    try:
        # Perform a semantic search using the query
        results = collection.query(
            query_texts=[input_data.query],
            n_results=5  # Return top 5 results
        )

        # Format the results
        formatted_results = []
        for metadatas_list, distances_list in zip(results['metadatas'], results['distances']):
            for metadata, score in zip(metadatas_list, distances_list):
                formatted_results.append({'content': metadata['content'], 'score': score})

        return {
            'message': 'Query executed successfully',
            'results': formatted_results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal error: {e}') from e
