from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models,tokens
from database import get_fastdb
from hashing import Hash

router= APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('')
def login(request: OAuth2PasswordRequestForm = Depends(), fastdb: Session = Depends(get_fastdb)):
    #or_(models.User.email == request.email,models.User.name == name)
    user = fastdb.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials(Password)')
    
    
    access_token = tokens.create_access_token(data={"sub": user.email})
    return {"access_token":access_token, "token_type":"bearer"}