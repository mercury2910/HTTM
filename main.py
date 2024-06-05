from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dto.product_dto import ProductDto
from knn_model import knn_model_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return HTTPException(status_code=500, detail=str(exc))

# Knn model suggestion products
@app.post("/suggest/product")
async def suggest(request: List[ProductDto]):
    suggest_products = await get_suggested_products(request)
    return suggest_products

async def get_suggested_products(request: List[ProductDto]):
    try:
        return await knn_model_service.suggest_product(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Configure OpenAPI and Redoc URLs
app.openapi_url = "/openapi.json"
app.redoc_url = "/redoc"

# Additional OpenAPI metadata (optional)
app.openapi_extra = {
    "info": {
        "title": "Your API Title",
        "description": "Your API Description",
        "version": "1.0"
    },
    "servers": [{"url": "http://localhost:8000", "description": "Local Development Server"}]
}