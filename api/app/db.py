from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.future import select

from app.conf import settings


async def get_db():
    """
    Creates async db client
    """
    engine = create_async_engine(str(settings.POSTGRES_URI), echo=False, future=True)
    session_local = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_local() as session:
        yield session


async def query_db(model: DeclarativeMeta, db: AsyncSession, **kwargs):
    """
    Takes async db session object and query using given model and filters
    :param model: SQLModel class
    :param db: AsyncSession object
    :param kwargs: arguments that will be used to filter result
    :return: session execute result
    """
    query = select(model)
    if kwargs:
        for attr, value in kwargs.items():
            query = query.where(getattr(model, attr) == value)
    return await db.execute(query)


async def get_db_object(model: DeclarativeMeta, db: AsyncSession | None = None, **kwargs):
    """
    Helper function used to query db for given the model. Accepts kwargs that will be used to filter result.
    Function accepts AsyncSession db object. If not passed, new session will be created.
    Using this approach, multiple db connection being created in one endpoint can be prevented. If session is created
    in the endpoint, we can simply pass session to this method to retrieve results. Otherwise, new connection will
    be created to retrieve results, without having to create connection in the endpoint itself.
    :param model: SQLModel class
    :param db: AsyncSession object
    :param kwargs: arguments that will be used to filter result
    :return: scalar result object. Can be called with .first() or .all() later
    """
    result = None
    if db:
        result = await query_db(model, db, **kwargs)
    else:
        async for db in get_db():
            result = await query_db(model, db, **kwargs)
    return result.scalars()
