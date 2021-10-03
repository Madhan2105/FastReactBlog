from pydantic import BaseModel,Field
from datetime import datetime, time, timedelta
from typing import Optional,List

class BlogSchema(BaseModel):
    title: str
    body: str
    file:Optional[str]
    created_at:datetime
    updated_at:datetime    
    slug:str
    is_active: Optional[bool] = None


class BlogList(BlogSchema):
    id:int
    class Config:
        orm_mode = True

class PaginatedBlogs(BaseModel):
    limit: int
    offset: int
    data: List[BlogList]


