from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, get_api_key
from .schemas import LLMQueryRequest, LLMQueryResponse, SimilaritySearchRequest
from openai import OpenAI
import os
from dotenv import load_dotenv
from .embeddings_router import similarity_search
from .rate_limiter import rate_limit

load_dotenv()

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/query", response_model=LLMQueryResponse)
@rate_limit(limit=10, period=3600)
async def llm_query(query_request: LLMQueryRequest, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        similarity_request = SimilaritySearchRequest(text=query_request.text, api_key=api_key)
        similarity_response = await similarity_search(similarity_request, db)
        context = similarity_response.result

        messages = [
            {"role": "system", "content": f"You are a helpful assistant. Use the following facts to inform your responses, but use the facts only if they match the context of the user prompt, if they don't - use your generic knowledge:\n\n{context}"},
            {"role": "user", "content": query_request.text}
        ]

        llm_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )

        return LLMQueryResponse(response=llm_response.choices[0].message.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")