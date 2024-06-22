<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="pgvector">
  <img src="https://img.shields.io/badge/SQLAlchemy%20⚗️-2B5B84?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <a href="https://docs.pydantic.dev/latest/contributing/#badges"><img src="https://img.shields.io/endpoint?style=for-the-badge&url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json" alt="Pydantic v2"></a>
  <img src="https://img.shields.io/badge/htmx-%23000000.svg?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTYgMjU2Ij48cGF0aCBkPSJNMTcwLjQgODUuNGwtNDIuNCA0Mi40LTQyLjQtNDIuNEw2NCA5Ni41bDQyLjQgNDIuNC00Mi40IDQyLjQgMjEuMiAyMS4yIDQyLjQtNDIuNCA0Mi40IDQyLjQgMjEuMi0yMS4yLTQyLjQtNDIuNCA0Mi40LTQyLjR6IiBmaWxsPSIjZmZmIi8+PC9zdmc+" alt="HTMX">
</div>

# TuskVector - API Platform 🐘

TuskVector is an API platform built to handle your data organization and retrieval needs. Why "TuskVector"? Well, just like an elephant's tusk, it's strong, reliable, and gets the job done. 📊

## Tech Stack 🛠️

TuskVector is powered by a mix of technologies:

- 🐍 Python for the backend (no surprises there)
- 🐘 pgvector for PostgreSQL vector database functionality (elephants, vectors and databases, get it?)
- ⚡ FastAPI for building APIs (gotta go fast!)
- 🛡️ Pydantic for data validation (because who doesn't love strict typing?)
- 🧪 SQLAlchemy for database integration (SQL is still cool, right?)
- 🌑 HTMX for the frontend to dodge JavaScript (because apparently, that's a thing now)

## Current Features 🎉

TuskVector offers a few API endpoints to manage your items:

- 🔍 Get an item by its ID using `GET /items/{item_id}`
- ➕ Create a new item with `POST /items`
- 🗑️ Delete an item by its ID using `DELETE /items/{item_id}`

Nothing groundbreaking, but hey, it works.

## Future Plans 🔮

The team behind TuskVector claims they'll integrate vector database functionality using pgvector soon. Apparently, this will allow for fast similarity searches and improve data querying capabilities. We'll believe it when we see it. 🚀

## Getting Started 🚀

If you want to give TuskVector a spin, check out the Swagger API documentation under /docs path. It should tell you everything you need to know about how to use the platform and its features. 📚

Whether you're a seasoned developer or a newbie, TuskVector aims to make your development process a bit less painful. No promises, though. 💪

Happy coding, I guess. 💻🐘
