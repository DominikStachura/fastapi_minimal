from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    is_active: bool | None


class Item(ItemBase):
    id: int
    is_active: bool = True
