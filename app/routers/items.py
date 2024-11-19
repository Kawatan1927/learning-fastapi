from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Query, Path

from app.models import Item, User

router = APIRouter()

fake_items_db = {
    1: {"name": "Item One", "price": 10.0, "description": "First item", "tax": 1.0},
    2: {"name": "Item Two", "price": 20.0, "description": "Second item", "tax": 2.0},
    3: {"name": "Item Three", "price": 30.0, "description": "Third item", "tax": 3.0},
}

fake_user_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice Wonderland",
        "address": [
            {"street": "Wonderland", "city": "New York", "zipcode": "10001"},
            {"street": "Mars", "city": "Mars", "zipcode": "00000"}
        ]
    },
    "bob": {
        "username": "bob",
        "email": "bob@example.com",
        "full_name": "Bob Builder",
        "address": []
    },
}


@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, min_price: Optional[float] = Query(None, ge=0), max_price: Optional[float] = Query(None, ge=0)):
    items = list(fake_items_db.values())[skip: skip + limit]
    if min_price is not None:
        items = [item for item in items if item["price"] >= min_price]
    if max_price is not None:
        items = [item for item in items if item["price"] <= max_price]
    return items


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int = Path(..., ge=1), q: Optional[str] = None):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item = fake_items_db[item_id]
    if q:
        item.update({"q": q})
    return item


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    new_id = max(fake_items_db.keys()) + 1
    fake_items_db[new_id] = {"name": item.name, "price": item.price, "description": item.description, "tax": item.tax}
    return fake_items_db[new_id]


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if user.username in fake_user_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    fake_user_db[user.username] = user.dict()
    return fake_user_db[user.username]
