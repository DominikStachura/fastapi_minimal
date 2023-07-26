import pytest
import httpx

from fastapi import status
from sqlalchemy import select

from app.models import ItemModel


@pytest.mark.asyncio
async def test_get_items(test_client: httpx.AsyncClient, item_in_db: ItemModel):
    response = await test_client.get("/item/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 1
    response_item = response_data[0]
    assert response_item["id"] == item_in_db.id
    assert response_item["name"] == item_in_db.name


@pytest.mark.asyncio
async def test_get_item(test_client: httpx.AsyncClient, item_in_db: ItemModel):
    response = await test_client.get(f"/item/{item_in_db.id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == item_in_db.id
    assert response_data["name"] == item_in_db.name


@pytest.mark.asyncio
async def test_create_item(test_client: httpx.AsyncClient, db):
    response = await test_client.post("/item/", json={"name": "created_item"})
    assert response.status_code == status.HTTP_200_OK
    created_item_id = response.json()["id"]
    created_item = (await db.execute(select(ItemModel).where(ItemModel.id == created_item_id))).scalar()
    assert created_item.name == "created_item"
    # should be true by default
    assert created_item.is_active is True


@pytest.mark.asyncio
async def test_create_item_already_exists(test_client: httpx.AsyncClient, item_in_db: ItemModel):
    response = await test_client.post("/item/", json={"name": item_in_db.name})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_update_item(test_client: httpx.AsyncClient, db, item_in_db: ItemModel):
    assert item_in_db.is_active is True
    await test_client.put(f"/item/{item_in_db.id}/", json={"is_active": False})
    await db.refresh(item_in_db)
    updated_item = (await db.execute(select(ItemModel).where(ItemModel.id == item_in_db.id))).scalar()
    assert updated_item.is_active is False


@pytest.mark.asyncio
async def test_update_item_not_exist(test_client: httpx.AsyncClient):
    response = await test_client.put("/item/999/", json={"is_active": False})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_item(test_client: httpx.AsyncClient, db, item_in_db: ItemModel):
    item = (await db.execute(select(ItemModel).where(ItemModel.id == item_in_db.id))).scalar()
    assert item
    await test_client.delete(f"/item/{item_in_db.id}/")
    deleted = (await db.execute(select(ItemModel).where(ItemModel.id == item_in_db.id))).scalar()
    assert not deleted


@pytest.mark.asyncio
async def test_delete_item_not_exist(test_client: httpx.AsyncClient):
    response = await test_client.delete("/item/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
