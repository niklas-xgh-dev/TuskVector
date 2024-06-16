from fastapi import FastAPI, Depends
from items_router import router as items_router
from database import get_db, Item

app = FastAPI()

# Add Swagger UI configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API",
        version="1.0.0",
        description="This is the API description.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.include_router(items_router)
app = FastAPI(docs_url="/docs", openapi_url="/api/openapi.json")

@app.get("/api/items")
def get_items(db=Depends(get_db)):
    items = db.exec(select(Item)).all()
    return items