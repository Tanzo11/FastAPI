from typing import List
from fastapi import FastAPI, Depends, status, Response , HTTPException
import schema, models
#from schema import User,Blog
#from models import User,Blog 
from database import engine, get_fastdb
from sqlalchemy.orm import Session
from hashing import Hash
from routers import blog

app = FastAPI()

models.Base.metadata.create_all(engine)


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

def create(request: schema.Blog,response=schema.ShowBlog,fastdb: Session = Depends(get_fastdb)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=2)
    fastdb.add(new_blog)
    fastdb.commit()
    fastdb.refresh(new_blog)
    return new_blog


#delete a blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])

def destroy(id, fastdb: Session = Depends(get_fastdb)):
    blogs = fastdb.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    fastdb.commit()
    return f'Blog id {id} deleted' 



#update a blog

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])

def update(id, request: schema.Blog ,fastdb: Session = Depends(get_fastdb)):
    
    blogs=fastdb.query(models.Blog).filter(models.Blog.id == id).update(dict(request))
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


@app.get('/blog/{id}',status_code=200,response_model=schema.ShowBlog, tags=['blogs'])

def show(id : int,response: Response,fastdb: Session = Depends(get_fastdb)):
    blogs = fastdb.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} is not available')
        
        '''response.status_code = status.HTTP_404_NOT_FOUND
        return {'details':f'Blog with the id {id} is not available'}'''
    return blogs
    








@app.post('/user', response_model=schema.ShowUser, tags=['user'])
def create_user(request: schema.User,fastdb: Session = Depends(get_fastdb)):
   
   new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),phone=request.phone)
   fastdb.add(new_user)
   fastdb.commit()
   fastdb.refresh(new_user)
   return new_user




@app.get('/user/{id}',response_model=schema.ShowUser, tags=['user'])

def get_user(id :int,fastdb: Session = Depends(get_fastdb)):
    users=fastdb.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} is not available')
    return users