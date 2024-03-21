from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_fastdb
from repository import nykaa

router = APIRouter(
    prefix='/nykaa',
    tags=['Nykaa']

)

@router.get("/search")
def search_keyword(keyword: str, fastdb: Session = Depends(get_fastdb)):
    return {"links": nykaa.search(keyword, fastdb)}