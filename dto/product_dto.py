from pydantic import BaseModel

class ProductDto(BaseModel):
    Age: int
    Gender: float
    Category: float
    PurchaseAmount: int