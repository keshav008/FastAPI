from fastapi import FastAPI
from typing import Optional
app=FastAPI()

@app.get('/blog')
def index(limit,published): #this will give if you do not provide the parameters
    if published:
        return {'data':f'{limit} published blogs'}
    else:
        return {'data':'f{limit} blogs'}
    
@app.get('/blog2')
def index2(limit: Optional[int]=None, published: Optional[str]=None):# this will not give any error if we do not give any parameter to this
    if published:
        return {'data': f'{limit} published blogs'}
    elif limit is not None:
        return {'data': f'{limit} blogs'}
    else:
        return {'data': 'All blogs'}