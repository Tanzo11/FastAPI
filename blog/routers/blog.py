from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
import models
from database import get_fastdb 
import oauth2
from repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']

)


@router.get('', response_model=List[models.ShowBlog])

def all(fastdb: Session = Depends(get_fastdb),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.get_all(fastdb)


@router.post('',status_code=status.HTTP_201_CREATED)

def create(request: models.Blog,response=models.ShowBlog,fastdb: Session = Depends(get_fastdb), current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.create(request,fastdb,current_user)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)

def destroy(id, fastdb: Session = Depends(get_fastdb),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id,fastdb)


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)

def update(id, request: models.Blog ,fastdb: Session = Depends(get_fastdb),current_user: models.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, fastdb)


@router.get('/{id}',status_code=200,response_model=models.ShowBlog)

def show(id : int,fastdb: Session = Depends(get_fastdb),current_user: models.User = Depends(oauth2.get_current_user)):    
    return blog.show(id,fastdb)