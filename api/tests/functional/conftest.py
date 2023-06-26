import pytest

from alembic.config import Config
from alembic import command


@pytest.fixture(autouse=True)
def make_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(autouse=True, scope="session")
def migrate_final():
    yield
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
