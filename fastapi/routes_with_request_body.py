from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

#defines the modal class which defines that what are the data parameters required

class Blog(BaseModel):#extended from basemodel
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(blog:Blog):#here Blog is the modal class name
    return {'data':f'blog is created with title as {blog.title} and body as {blog.body}'}