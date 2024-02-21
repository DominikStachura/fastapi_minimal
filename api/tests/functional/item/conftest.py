import pytest_asyncio

from app.schemas.item import Item


@pytest_asyncio.fixture
async def item_in_db(db):
    item = Item(
        name="test_item"
    )
    db.add(item)
    await db.commit()
    yield item
