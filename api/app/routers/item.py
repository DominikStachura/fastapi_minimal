from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.db import get_db
from app.schemas.item import ItemUpdate, Item, ItemCreate

router = APIRouter(
    prefix="/item",
    tags=["item"]
)


@router.post("/", response_model=Item)
async def create_item(item: ItemCreate, db=Depends(get_db)):
    """
    Creates new item in the database
    """
    if (await db.execute(select(Item).where(Item.name == item.name))).scalar():
        raise HTTPException(detail="Item already exists.", status_code=status.HTTP_400_BAD_REQUEST)
    item_object = Item(**item.dict())
    db.add(item_object)
    await db.commit()
    return item_object


@router.get("/{item_id}/")
async def get_item(item_id: int, db=Depends(get_db)) -> Item:
    """
    Get item with the given ID
    """
    item_in_db = (await db.execute(select(Item).where(Item.id == item_id))).scalar()
    return item_in_db


@router.get("/")
async def list_items(db=Depends(get_db)) -> list[Item]:
    """
    Get item with the given ID
    """
    items = (await db.execute(select(Item))).scalars().all()
    return items


@router.put("/{item_id}/")
async def update_item(item_id: int, item: ItemUpdate, db=Depends(get_db)) -> Item:
    """
    Updates item information, such as is_active
    """
    item_in_db = (await db.execute(select(Item).where(Item.id == item_id))).scalar()
    if not item_in_db:
        raise HTTPException(detail=f"Item with id {item_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    put_data = item.dict(exclude_unset=True)
    for key, value in put_data.items():
        setattr(item_in_db, key, value)
    db.add(item_in_db)
    await db.commit()
    return item_in_db


@router.delete("/{item_id}/")
async def delete_item(item_id: int, db=Depends(get_db)) -> Item:
    """
    Deletes item with the given ID
    """
    item_in_db = (await db.execute(select(Item).where(Item.id == item_id))).scalar()
    if not item_in_db:
        raise HTTPException(detail=f"Item with id {item_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(item_in_db)
    await db.commit()
    return item_in_db
