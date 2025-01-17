import chromadb
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


# Initialize the embedding model and vector database
model = SentenceTransformer('all-MiniLM-L6-v2')
vector_db = chromadb.HttpClient(host='http://vector-db:8000')

# Create or retrieve a collection
collection = vector_db.get_or_create_collection('html_embeddings')

# FastAPI configuration
app = FastAPI()


# Input model
class UrlInput(BaseModel):
    """
    Input model for the /process-url endpoint.
    """
    url: str


def extract_text_from_url(url: str, min_length: int = 100) -> list[str]:
    """
    Extracts meaningful text content from a given URL while filtering out short paragraphs.

    Args:
        url (str): The URL to fetch and process.
        min_length (int): The minimum length (in characters) for paragraphs to be included.

    Returns:
        list[str]: A list of paragraphs that meet the minimum length requirement.

    Raises:
        ValueError: If the content is not HTML or the request fails.
    """
    try:
        # Make the HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Check the returned content type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            raise ValueError('The URL content is not HTML.')

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        # Remove unnecessary tags
        for tag in soup(['script', 'style', 'meta', 'noscript']):
            tag.decompose()

        # List of inline tags to unwrap, keeping their text content
        tags_to_unwrap = [
            'strong', 'span', 'b', 'em', 'i', 'u', 'mark', 'a',
            'small', 'sub', 'sup', 'abbr', 'code', 'time'
        ]

        # Remove the specified tags while preserving their inner text
        for tag in soup.find_all(tags_to_unwrap):
            tag.unwrap()

        # Extract text with '\n' as the separator
        raw_text = soup.get_text(separator='').strip()

        # Split text into paragraphs
        paragraphs = raw_text.split('\n')

        # Filter out short paragraphs
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) >= min_length]

        return paragraphs
    except Exception as e:
        raise ValueError(f'Error processing the URL: {e}') from e


@app.get('/')
def read_root():
    """
    Health check endpoint for the API.

    Returns:
        dict: A dictionary containing the status of the service.
    """
    return {'status': 'running'}


@app.post('/process-url')
async def process_url(input_data: UrlInput):
    """
    Processes a URL by extracting meaningful text, generating embeddings, 
    and storing the embeddings in the vector database.

    Args:
        input_data (UrlInput): Input data containing the URL to process.

    Returns:
        dict: A dictionary with the processing status, number of paragraphs, and the extracted paragraphs.

    Raises:
        HTTPException: If the URL content is invalid or an internal error occurs.
    """
    try:
        # Extract text from the URL
        paragraphs = extract_text_from_url(input_data.url)

        # Generate embeddings
        embeddings = [
            {
                'embedding': model.encode(paragraph).tolist(),
                'metadata': {'content': paragraph}
            }
            for paragraph in paragraphs if paragraph.strip()
        ]

        # Save the embeddings in the vector database collection
        for embedding in embeddings:
            collection.add(
                embeddings=[embedding['embedding']],
                metadatas=[embedding['metadata']],
                ids=[str(hash(embedding['metadata']['content']))]
            )

        return {
            'message': 'URL processed successfully!',
            'num_paragraphs': len(embeddings),
            'paragraphs': paragraphs
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal error: {e}') from e
