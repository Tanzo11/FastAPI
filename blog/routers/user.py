from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_fastdb 
from hashing import Hash
from repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']

)

@router.post('', response_model=models.UserCreate)

def create(request: models.User,fastdb: Session = Depends(get_fastdb)):
    return user.create(request,fastdb)




@router.get('/{id}',response_model=models.ShowUser)

def get_user(id :int,fastdb: Session = Depends(get_fastdb)):
    return user.get(id,fastdb)