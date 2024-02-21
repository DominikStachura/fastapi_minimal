from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    name: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    is_active: bool | None


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_active: bool = True
