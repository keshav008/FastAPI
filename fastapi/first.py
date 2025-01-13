from fastapi import FastAPI

app=FastAPI()

@app.get('/testing_api')
def index():
    return {"message":"welcome to the fastapi"}