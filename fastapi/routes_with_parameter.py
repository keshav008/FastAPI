from fastapi import FastAPI

app=FastAPI()

#routes with parameter
@app.get('/blog/{id}')
def blog(id:int): #defining that id parameter should be of integer type only using pydantic thing
    return {'data':id}