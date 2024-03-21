from fastapi import Depends, HTTPException, status
import tokens,schema
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from tokens import ALGORITHM, SECRET_KEY
from sqlalchemy.orm import Session




class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication sheme.")
            if self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expiredd token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwttoken: str) -> bool:
        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except (JWTError, ExpiredSignatureError):
            return False
        
oauth2_scheme = JWTBearer()    

def get_current_user(token: str= Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = tokens.verify_token(token,credentials_exception)
    return email

