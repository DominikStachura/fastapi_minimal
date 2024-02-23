from fastapi import APIRouter, Depends, HTTPException, status

from app.db import get_db, get_db_object
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
    if (await get_db_object(Item, db, name=item.name)).first():  # type: ignore
        raise HTTPException(detail="Item already exists.", status_code=status.HTTP_400_BAD_REQUEST)
    item_object = Item(**item.model_dump())
    db.add(item_object)
    await db.commit()
    return item_object


@router.get("/{item_id}/")
async def get_item(item_id: int) -> Item:
    """
    Get item with the given ID
    """
    item_in_db = (await get_db_object(Item, id=item_id)).first()
    if not item_in_db:
        raise HTTPException(detail=f"Item with id {item_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return item_in_db


@router.get("/")
async def list_items() -> list[Item]:
    """
    Get item with the given ID
    """
    items = (await get_db_object(Item)).all()
    return items


@router.put("/{item_id}/")
async def update_item(item_id: int, item: ItemUpdate, db=Depends(get_db)) -> Item:
    """
    Updates item information, such as is_active
    """
    item_in_db = (await get_db_object(Item, db, id=item_id)).first()
    if not item_in_db:
        raise HTTPException(detail=f"Item with id {item_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    put_data = item.model_dump(exclude_unset=True)
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
    item_in_db = (await get_db_object(Item, db, id=item_id)).first()
    if not item_in_db:
        raise HTTPException(detail=f"Item with id {item_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(item_in_db)
    await db.commit()
    return item_in_db
