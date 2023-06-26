from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ColumnDefault

Base = declarative_base()


class ItemModel(Base):
    """
    SQLAlchemy Model for Item used to interact with the DataBase
    """
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=ColumnDefault(True))
