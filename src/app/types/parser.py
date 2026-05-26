from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str | None
    price: str | None
    description: str
    image: str | None
    url: str | None