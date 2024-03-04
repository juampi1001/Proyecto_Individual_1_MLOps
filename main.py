from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """
    Proyecto FastAPI - Sistema de Recomendaciones

    Versión: 1.0.0

    ---

    """
    return {"Mensaje": "Proyecto Individual N° 1 - Juan Pablo Vitalevi"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
