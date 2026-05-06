from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: str
    description: str
    image: str
    url: str