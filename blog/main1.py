from typing import List
from fastapi import FastAPI, Depends, status, Response , HTTPException
import models, schema
#from schema import User,Blog
#from models import User,Blog 
from database import engine, get_fastdb
from sqlalchemy.orm import Session
from hashing import Hash
from routers import blog

app = FastAPI()

schema.Base.metadata.create_all(engine)


app.include_router(blog.router)

"""def get_fastdb():
    fastdb = SessionLocal()
    try:
        yield fastdb
    finally:
        fastdb.close"""



#insert into the database
        
#@app.post('/blog',status_code=201)
        
@app.post('/blog',status_code=status.HTTP_201_CREATED, tags=['blogs'])

def create(request: models.Blog,response=models.ShowBlog,fastdb: Session = Depends(get_fastdb)):
    new_blog = schema.Blog(title=request.title,body=request.body,user_id=2)
    fastdb.add(new_blog)
    fastdb.commit()
    fastdb.refresh(new_blog)
    return new_blog


#delete a blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])

def destroy(id, fastdb: Session = Depends(get_fastdb)):
    blogs = fastdb.query(schema.Blog).filter(schema.Blog.id == id).delete(synchronize_session=False)
    fastdb.commit()
    return f'Blog id {id} deleted' 



#update a blog

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])

def update(id, request: models.Blog ,fastdb: Session = Depends(get_fastdb)):
    
    blogs=fastdb.query(schema.Blog).filter(schema.Blog.id == id).update(dict(request))
    #blogs.update({'title':'updated title'}) #will change to 'updated title'
    #update with the change made in schema

    fastdb.commit()
    return 'Updated Successfully'




#get from the database

"""@app.get('/blog', response_model=List[schema.ShowBlog], tags=['blogs'])

            #adding the response will give the response model
def all(fastdb: Session = Depends(get_fastdb)):
    blogs = fastdb.query(models.Blog).all()
    return blogs"""


@app.get('/blog/{id}',status_code=200,response_model=models.ShowBlog, tags=['blogs'])

def show(id : int,response: Response,fastdb: Session = Depends(get_fastdb)):
    blogs = fastdb.query(schema.Blog).filter(schema.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
        
        '''response.status_code = status.HTTP_404_NOT_FOUND
        return {'details':f'Blog with the id {id} is not available'}'''
    return blogs
    








@app.post('/user', response_model=models.ShowUser, tags=['user'])
def create_user(request: models.User,fastdb: Session = Depends(get_fastdb)):
   
   new_user = schema.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),phone=request.phone)
   fastdb.add(new_user)
   fastdb.commit()
   fastdb.refresh(new_user)
   return new_user




@app.get('/user/{id}',response_model=models.ShowUser, tags=['user'])

def get_user(id :int,fastdb: Session = Depends(get_fastdb)):
    users=fastdb.query(schema.User).filter(schema.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} is not available')
    return users