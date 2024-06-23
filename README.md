<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="pgvector">
  <img src="https://img.shields.io/badge/SQLAlchemy%20⚗️-2B5B84?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <a href="https://docs.pydantic.dev/latest/contributing/#badges"><img src="https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json" alt="Pydantic v2"></a>
  <img src="https://img.shields.io/badge/htmx-%23000000.svg?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTYgMjU2Ij48cGF0aCBkPSJNMTcwLjQgODUuNGwtNDIuNCA0Mi40LTQyLjQtNDIuNEw2NCA5Ni41bDQyLjQgNDIuNC00Mi40IDQyLjQgMjEuMiAyMS4yIDQyLjQtNDIuNCA0Mi40IDQyLjQgMjEuMi0yMS4yLTQyLjQtNDIuNCA0Mi40LTQyLjR6IiBmaWxsPSIjZmZmIi8+PC9zdmc+" alt="HTMX">
</div>

# TuskVector - API Platform 🐘

TuskVector is an API platform built to handle your data organization and retrieval needs. Why "TuskVector"? Well, just like an elephant's tusk, it's strong, reliable, and gets the job done. Plus, it now remembers things almost as well as an elephant. Almost. 📊🧠

## Tech Stack 🛠️

TuskVector is powered by a mix of technologies:

- 🐍 Python for the backend (no surprises there)
- 🐘 pgvector for Postgre DB vector functionality (elephants and vectors, get it?)
- ⚡ FastAPI for building APIs (gotta go fast!)
- 🛡️ Pydantic for data validation (because who doesn't love strict typing?)
- 🧪 SQLAlchemy for database integration (SQL is still cool, right?)
- 🌑 HTMX as frontend to dodge JavaScript (because apparently, that's a thing now)
- 🤖 OpenAI for embeddings and LLM queries (because why think when AI can do it for you?)

## Current Features 🎉
TuskVector now offers a bunch of API endpoints to manage your items and queries:

- 🔍 Get an item by its ID using GET /api/items/{item_id}
- ➕ Create a new item with POST /api/items
- 🗑️ Delete an item by its ID using DELETE /api/items/{item_id}
- 📥 Embed and store facts with POST /api/embed_text
- 🔎 Find similar facts using POST /api/similarity_search
- 🧠 Query an LLM with facts as context using POST /api/query

We've gone from "nothing groundbreaking" to "kinda cool", so that's progress, right?

## Vector Magic ✨

Remember when we said we'd integrate vector database functionality? Well, we actually did it! TuskVector now uses pgvector for fast similarity searches. It's like finding a needle in a haystack, if the needle was a piece of text and the haystack was your database. 🧭

## Getting Started 🚀

If you want to give TuskVector a spin, check out the Swagger API documentation under /docs path. It should tell you everything you need to know about how to use the platform and its features. Or you could just guess and hope for the best. Your choice. 📚

## Future Plans 🔮

The team behind TuskVector is thinking about adding more features. They're not sure what yet, but we're not holding our breath. 😉
May your queries be fast and your embeddings be meaningful. 💻🐘