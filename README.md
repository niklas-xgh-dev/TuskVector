<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="pgvector">
  <img src="https://img.shields.io/badge/HNSW-FF6B6B?style=for-the-badge&logo=graphql&logoColor=white" alt="HNSW">
  <img src="https://img.shields.io/badge/OpenAI%20ada2-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI ada2">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/htmx-%23000000.svg?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTYgMjU2Ij48cGF0aCBkPSJNMTcwLjQgODUuNGwtNDIuNCA0Mi40LTQyLjQtNDIuNEw2NCA5Ni41bDQyLjQgNDIuNC00Mi40IDQyLjQgMjEuMiAyMS4yIDQyLjQtNDIuNCA0Mi40IDQyLjQgMjEuMi0yMS4yLTQyLjQtNDIuNCA0Mi40LTQyLjR6IiBmaWxsPSIjZmZmIi8+PC9zdmc+" alt="HTMX">
</div>

# TuskVector - API Platform 🐘

This API framework first transforms your data in 1536D vectors (as RAGs do), then employs HNSW indexing for efficient information retrieval (again, as RAGs do) using pgvector. In short - it enhances your database with search capabilities before plugging it into further queries. Check it out on https://tuskvector.com

## Tech Stack 

TuskVector is built with:

- Python for the backend (no surprises there)
- pgvector for Postgre DB vector functionality (elephants and vectors, get it?)
- HNSW for fast approximate nearest neighbor search
- OpenAI's ada2 for text embeddings
- GPT 4o for LLM queries 
- FastAPI for building APIs
- HTMX as frontend to dodge JavaScript (because apparently, that's a thing now)


### API Endpoints - also found on https://tuskvector.com/docs

1. **Vector Embedding (POST `/api/embed_text`)**
   - Utilizes OpenAI's text-embedding-ada-002 model
   - Generates 1536-dimensional embeddings
   - Automatically stores embeddings in pgvector-enabled PostgreSQL database

2. **Similarity Search (POST `/api/similarity_search`)**
   - Implements cosine similarity metric
   - Utilizes HNSW (Hierarchical Navigable Small World) index for approximate nearest neighbor search
   - Configurable search parameters:
     - `ef_search`: Controls the trade-off between search speed and accuracy
     - Distance threshold: Filters results based on maximum allowed cosine distance

3. **Context-Aware LLM Queries (POST `/api/query`)**
   - Integrates with OpenAI's GPT models
   - Enhances LLM responses with relevant context from the vector database
   - Implements a two-stage retrieval process:
     1. Vector similarity search to find relevant facts
     2. LLM query augmented with retrieved context

### Configuration Options

- `HNSW_M`: Maximum number of connections per layer in HNSW index (we went with 16)
- `HNSW_EF_CONSTRUCTION`: Size of the dynamic candidate list for constructing the HNSW graph (we went with 64)
- `MAX_DISTANCE`: Cosine distance threshold for similarity search (we went with 0.1)
