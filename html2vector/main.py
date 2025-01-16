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
    url: str


# Function to verify if the content is HTML and extract text
def extract_text_from_url(url: str) -> str:
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
        
        # Extract and return the clean text
        return soup.get_text(separator='\n').strip()
    except Exception as e:
        raise ValueError(f'Error processing the URL: {e}')


@app.get('/')
def read_root():
    return {'status': 'running'}


# Endpoint to process the URL
@app.post('/process-url')
async def process_url(input_data: UrlInput):
    try:
        # Extract text from the URL
        text = extract_text_from_url(input_data.url)
        
        # Split the text into paragraphs and generate embeddings
        paragraphs = text.split('\n')
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
            'content': text,
            'embeddings': embeddings
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal error: {e}')
