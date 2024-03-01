from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schema
from database import get_fastdb 
import models
from hashing import Hash
from repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']

)

@router.post('', response_model=schema.ShowUser)

def create(request: schema.User,fastdb: Session = Depends(get_fastdb)):
    return user.create(request,fastdb)




@router.get('/{id}',response_model=schema.ShowUser)

def get_user(id :int,fastdb: Session = Depends(get_fastdb)):
    return user.get(id,fastdb)