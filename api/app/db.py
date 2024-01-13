from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.conf import settings


async def get_db():
    """
    Creates async db client
    """
    engine = create_async_engine(str(settings.POSTGRES_URI), echo=False, future=True)
    session_local = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_local() as session:
        yield session
