from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_db, get_api_key
from .rate_limiter import rate_limit
from .schemas import TextEmbeddingCreate, TextEmbeddingResponse, SimilaritySearchRequest, SimilaritySearchResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/embed_text", response_model=TextEmbeddingResponse)
@rate_limit(limit=10, period=3600)
async def embed_text(text_input: TextEmbeddingCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        # Generate embedding
        response = client.embeddings.create(
            input=text_input.text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding

        # Insert new embedding
        query = text("""
            INSERT INTO text_embeddings (text, embedding)
            VALUES (:text, :embedding)
            RETURNING id, text, created_at
        """)
        result = db.execute(query, {"text": text_input.text, "embedding": embedding})
        new_embedding = result.fetchone()
        db.commit()

        return TextEmbeddingResponse(
            id=new_embedding.id,
            text=new_embedding.text,
            created_at=new_embedding.created_at
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/similarity_search", response_model=SimilaritySearchResponse)
@rate_limit(limit=10, period=3600)
async def similarity_search(search_request: SimilaritySearchRequest, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        response = client.embeddings.create(
            input=search_request.text,
            model="text-embedding-ada-002"
        )
        search_embedding = response.data[0].embedding

        # Set HNSW search parameters
        ef_search = 64  # Increase for better recall at the cost of speed

        # Set session-level parameters
        db.execute(text("SET LOCAL hnsw.ef_search = :ef_search"), {"ef_search": ef_search})

        query = text("""
            SELECT text, embedding <=> CAST(:search_embedding AS vector) AS distance
            FROM text_embeddings
            ORDER BY embedding <=> CAST(:search_embedding AS vector)
            LIMIT 5
        """)
        results = db.execute(query, {"search_embedding": search_embedding}).fetchall()

        # Filter results that are not exceeding a minimal distance between the search and result vector
        max_distance = 0.1
        similar_texts = [result.text for result in results if result.distance < max_distance]

        if not similar_texts:
            return SimilaritySearchResponse(result="No sufficiently similar facts/texts found.")

        combined_text = "\n\n[FACT]\n".join(similar_texts)
        combined_text = f"[FACT]\n{combined_text}\n[/FACT]"

        return SimilaritySearchResponse(result=combined_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")