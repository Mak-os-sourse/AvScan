from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str | None
    price: str | None
    description: str
    image: str | None
    url: str | None