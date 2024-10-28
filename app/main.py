from fastapi import FastAPI, HTTPException

from typing import Optional

from .models import Item

app = FastAPI()

fake_items_db = {
    1: {"name": "item1", "price": 100},
    2: {"name": "item2", "price": 100},
}


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item = fake_items_db[item_id]
    if q:
        item.update({"q": q})
    return item


@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_tax": item.tax}
