from sqlalchemy.orm import Session
import schema , models
from fastapi import HTTPException, status

def get_all(fast_db: Session):
    blogs = fast_db.query(schema.Blog).all()
    return blogs


def create(request: models.Blog,fastdb: Session,current_user):
    user = fastdb.query(schema.User).filter(schema.User.email == current_user).first()
    new_blog = schema.Blog(title=request.title,body=request.body,user_id=user.id)
    fastdb.add(new_blog)
    fastdb.commit()
    fastdb.refresh(new_blog)
    return new_blog


def destroy(id: int, fastdb: Session):
    blogs = fastdb.query(schema.Blog).filter(schema.Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog id {id} deleted')
    blogs.delete(synchronize_session=False)
    fastdb.commit()
    return 'done'

def update(id: int, request:models.Blog, fastdb: Session):
    blogs=fastdb.query(schema.Blog).filter(schema.Blog.id == id).update(dict(request))
    fastdb.commit()
    return 'Updated Successfully'


def show(id: int,fastdb: Session):
    blogs = fastdb.query(schema.Blog).filter(schema.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
        
    return blogs