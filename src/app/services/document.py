import pandas as pd
from io import BytesIO
from dataclasses import asdict

from src.app.types.parser import Product

def create_product_document(products: list[Product]) -> bytes:
    df = pd.DataFrame([asdict(item) for item in products])
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()