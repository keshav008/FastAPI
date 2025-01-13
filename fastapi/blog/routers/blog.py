import sys
from pathlib import Path

# Add the parent folder to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import APIRouter, HTTPException, Depends,status,Response
import schemas
import models
import database
from sqlalchemy.orm import Session
import oauth2

router= APIRouter(
    tags=['Blogs']
)


@router.get('/all_blogs')# this will get all the blogs from the database
def get_blogs(db:Session=Depends(database.get_db), current_user:schemas.user=Depends(oauth2.get_current_user)):# current_user is given to protect our route behind the token 
    blogs=db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=status.HTTP_201_CREATED)# for creating the new blog with status code
def create(request: schemas.Blog, db: Session=Depends(database.get_db)):#function to create the new blog and insert that into the table 
    new_blog=models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Showblog)# this will give the blog using id with the Showblog response modela\
def show_blog(id: int, response:Response, db :Session=Depends(database.get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with id {id} is not available')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':'blog not found'}
    return blog

@router.delete('/delete_blog/{id}' , status_code=status.HTTP_204_NO_CONTENT) #for delete the blog 
def delete_blog(id:int, response:Response, db:Session=Depends(database.get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} is not availble')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'status':'deleted'}


@router.put('/update_blog/{id}' , status_code=status.HTTP_202_ACCEPTED) # for updating the particular blog using id
def update_blog(id: int, request:schemas.Blog, db:Session= Depends(database.get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id== id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} is not found')
    
    blog.update({'title':request.title,'body':request.body})
    db.commit()
    return {'message':'updated successfully'}

