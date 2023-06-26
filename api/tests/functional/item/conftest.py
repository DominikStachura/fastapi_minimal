import pytest_asyncio

from app.models import ItemModel


@pytest_asyncio.fixture
async def item_in_db(db):
    item = ItemModel(
        name="test_item"
    )
    db.add(item)
    await db.commit()
    yield item
