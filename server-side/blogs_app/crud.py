from typing import List
from sqlalchemy.orm import Session
from blogs_app.exception import BlogInfoNotFoundError, BlogInfoInfoAlreadyExistError
from .models import BlogsModel
from .schemas import BlogSchema

def get_all_blogs(session: Session,limit:int,offset:int)->List[BlogsModel]:    
    return session.query(BlogsModel).filter(BlogsModel.is_active==1).all()

def get_single_blog(session: Session,slug:str):
    print("sdfsdfsfdsdfdfsdaasdssdf/",slug)
    blog = session.query(BlogsModel).filter(BlogsModel.slug==slug,BlogsModel.is_active==1).first()    
    print("blog",blog)
    if blog is None:
        raise BlogInfoNotFoundError
    return blog

def create_blog(session: Session,blog_info:BlogSchema):
    print(blog_info,type(blog_info))
    blog_details = session.query(BlogsModel).filter(BlogsModel.slug == blog_info['slug']).first()
    print("creat blog",blog_details)
    if blog_details is not None:
        raise BlogInfoInfoAlreadyExistError
    new_blog_info = BlogsModel(**blog_info)     
    print("new_blog_info",new_blog_info)
    session.add(new_blog_info)
    session.commit()
    session.refresh(new_blog_info)
    return new_blog_info

def delete_blog(session:Session,_id:int):
    blog = session.query(BlogsModel).filter(BlogsModel.id==_id,BlogsModel.is_active==1).first()    
    if blog is None:
        raise BlogInfoNotFoundError
    blog.is_active = 0
    session.commit()
    session.refresh(blog)
    return blog


