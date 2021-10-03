from fastapi import APIRouter, Depends, HTTPException, File, UploadFile,Form
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import Null
from config.db import get_db
from .schemas import BlogSchema
from blogs_app.crud import get_all_blogs,get_single_blog,create_blog,delete_blog
from fastapi_utils.cbv import cbv
from blogs_app.exception import BlogInfoException,BlogInfoInfoAlreadyExistError
import shutil
import os
import base64
from typing import Optional
router = APIRouter()


# Example of Class based view

@cbv(router)
class Blogs:
    session: Session = Depends(get_db)

    @router.get("/all_blogs/")
    def get_all_blog(self, limit: int = 10, offset: int = 0):
        blogs_list = get_all_blogs(self.session,limit,offset)
        response = {"data": blogs_list}
        return response

    @router.get("/read_blog/{blog_id}")
    def get_single_blog(self, blog_id):
        try:
            single_blog = get_single_blog(self.session,blog_id)
            print("single_blog",single_blog)
            response = {"data": [single_blog]}
            return response
        except BlogInfoException as cie:
            raise HTTPException(**cie.__dict__)
    @router.post("/add_blog")
    def add_blog(self,blog_info: BlogSchema):

        try:
            blog_info = create_blog(self.session,blog_info)
            return blog_info
        except BlogInfoException as cie:
            raise HTTPException(**cie.__dict__)

    @router.delete("/delete_blog/{blog_id}")
    def delete_car(self,blog_id: int):
        try:
            return delete_blog(self.session, blog_id)
        except BlogInfoException as cie:
            raise HTTPException(**cie.__dict__)

@router.post("/add_blog/")
async def create_upload_file(
    session: Session = Depends(get_db),
    title: str = Form(...),
    body: str = Form(...),
    created_at: Optional[str] = Form(None),
    updated_at: Optional[str] = Form(None),
    slug: str = Form(...),
    is_active:str = Form(...),
    file: Optional[UploadFile] = File(None)
    ):
    if(file):
            
        file_path = os.getcwd() + "/my-react-blog-app/public/images/"+file.filename
        file_store_path = "/images/"+file.filename
        print("file_path",file_path)
        file_path_encode = file_store_path.encode("ascii")
        base64_bytes = base64.b64encode(file_path_encode)
        base64_string = base64_bytes.decode("ascii")    
    else:
        base64_string = None
        
    blog_info = {
        "title":title,
        "body":body,
        "created_at":created_at,
        "updated_at":updated_at,
        "slug":slug,
        "is_active":int(is_active),
        "file":base64_string
    }
    try:
        blog_info = create_blog(session,blog_info)
        if(file):
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
    except BlogInfoException as cie:
        raise HTTPException(**cie.__dict__)    
    return blog_info