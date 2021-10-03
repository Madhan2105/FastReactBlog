from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.types import String, Integer, Enum,DateTime
from config.db import Base
import enum

class BlogsModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    file = Column(String) 
    title = Column(String)
    body = Column(String)
    slug = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)