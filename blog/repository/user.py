from fastapi import status, HTTPException
from sqlalchemy.orm import Session
import schema, models
from hashing import Hash

def create(request,fastdb: Session):
    existing_user = fastdb.query(schema.User).filter(schema.User.email == request.email).first()
    if existing_user:
        # raise HTTPException(status_code=400, detail="User with this email already exists")
        return {"message": "User already exists", "user": None}

    new_user = schema.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),phone=request.phone)
    fastdb.add(new_user)
    fastdb.commit()
    fastdb.refresh(new_user)
    return {"message": "User Created", "user": new_user}

def get(id: int,fastdb: Session):
    users=fastdb.query(schema.User).filter(schema.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} is not available')
    return users