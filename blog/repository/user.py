from fastapi import status, HTTPException
from sqlalchemy.orm import Session
import models, schema
from hashing import Hash

def create(request,fastdb: Session):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),phone=request.phone)
    fastdb.add(new_user)
    fastdb.commit()
    fastdb.refresh(new_user)
    return new_user

def get(id: int,fastdb: Session):
    users=fastdb.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} is not available')
    return users