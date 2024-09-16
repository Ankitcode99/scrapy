from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    _id: Optional[str]=''
    generated_id: str
    product_title: str
    product_price: float
    path_to_image: str