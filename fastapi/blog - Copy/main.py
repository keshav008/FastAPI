from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Blog
import models
from schemas import Blog, Showblog #importing the Blog class from schemas.py file
import schemas
from hashing import Hash


models.Base.metadata.create_all(engine) #this will create a table mapped to models file
app= FastAPI()

def get_db(): #function to create the db in this file
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',tags=['Blogs'], status_code=status.HTTP_201_CREATED)# for creating the new blog with status code
def create(request: Blog, db: Session=Depends(get_db)):#function to create the new blog and insert that into the table 
    new_blog=models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/all_blogs', tags=['Blogs'])# this will get all the blogs from the database
def get_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',tags=['Blogs'], status_code=status.HTTP_200_OK, response_model=Showblog)# this will give the blog using id with the Showblog response modela\
def show_blog(id: int, response:Response, db :Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with id {id} is not available')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':'blog not found'}
    return blog

@app.delete('/delete_blog/{id}', tags=['Blogs'], status_code=status.HTTP_204_NO_CONTENT) #for delete the blog 
def delete_blog(id:int, response:Response, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} is not availble')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'status':'deleted'}


@app.put('/update_blog/{id}', tags=['Blogs'], status_code=status.HTTP_202_ACCEPTED) # for updating the particular blog using id
def update_blog(id: int, request:Blog, db:Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id== id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} is not found')
    
    blog.update({'title':request.title,'body':request.body})
    db.commit()
    return {'message':'updated successfully'}



@app.post('/create_user',tags=['Users'])
def create_user(request:schemas.user, db:Session=Depends(get_db)):# this will create a new user and insert into the database users table
    #hashed_password=pwd_cxt.hash(request.password)#encryptting the password
    new_user=models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/show_users', tags=['Users'] )#getting all the users from the database
def get_all_users(db:Session=Depends(get_db)):
    all_users=db.query(models.User).all()
    return all_users


@app.get('/user/{id}', tags=['Users'],response_model=schemas.Showuser)# get the user with id using reponse model
def get_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not available')
    return user