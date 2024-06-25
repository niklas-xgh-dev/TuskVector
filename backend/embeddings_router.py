from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db, TextEmbedding, get_api_key
from schemas import TextEmbeddingCreate, TextEmbeddingResponse, SimilaritySearchRequest, SimilaritySearchResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/embed_text", response_model=TextEmbeddingResponse)
async def embed_text(text_input: TextEmbeddingCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        response = client.embeddings.create(
            input=text_input.text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding

        new_embedding = TextEmbedding(
            text=text_input.text,
            embedding=embedding
        )

        db.add(new_embedding)
        db.commit()
        db.refresh(new_embedding)

        return TextEmbeddingResponse(
            id=new_embedding.id,
            text=new_embedding.text,
            created_at=new_embedding.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/similarity_search", response_model=SimilaritySearchResponse)
async def similarity_search(search_request: SimilaritySearchRequest, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        response = client.embeddings.create(
            input=search_request.text,
            model="text-embedding-ada-002"
        )
        search_embedding = response.data[0].embedding

        query = text("""
            SELECT text
            FROM text_embeddings
            ORDER BY embedding <=> CAST(:search_embedding AS vector)
            LIMIT 3
        """)
        results = db.execute(query, {"search_embedding": search_embedding}).fetchall()

        similar_texts = [result[0] for result in results]
        combined_text = "\n\n[FACT]\n".join(similar_texts)
        combined_text = f"[FACT]\n{combined_text}\n[/FACT]"

        return SimilaritySearchResponse(result=combined_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")