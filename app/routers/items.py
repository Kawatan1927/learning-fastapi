from fastapi import APIRouter, HTTPException

from app.models import Item

router = APIRouter()

fake_items_db = {
    1: {"name": "Item One", "price": 10.0},
    2: {"name": "Item Two", "price": 20.0},
}


@router.get("/")
def read_items(skip: int = 0, limit: int = 10):
    items = list(fake_items_db.values())[skip: skip + limit]
    return items


@router.get("/{item_id}")
def read_item(item_id: int, q: str = None):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item = fake_items_db[item_id]
    if q:
        item.update({"q": q})
    return item


@router.post("/")
def create_item(item: Item):
    new_id = max(fake_items_db.keys()) + 1
    fake_items_db[new_id] = {"name": item.name, "price": item.price}
    return {"item_id": new_id, "item": fake_items_db[new_id]}
