from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    description: str = Field(default="", max_length=1000)
    quantity: int = Field(default=0, ge=0)
    price: float = Field(default=0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    category: Optional[str] = Field(default=None, min_length=1, max_length=80)
    description: Optional[str] = Field(default=None, max_length=1000)
    quantity: Optional[int] = Field(default=None, ge=0)
    price: Optional[float] = Field(default=None, ge=0)

class StockUpdate(BaseModel):
    quantity_change: int
    # Positive value adds stock; negative value removes stock.

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str
    description: str
    quantity: int
    price: float
    created_at: str
    updated_at: str
