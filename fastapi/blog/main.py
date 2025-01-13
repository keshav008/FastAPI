from fastapi import FastAPI
from database import SessionLocal, engine
import models
from routers.blog import router as blogrouter
from routers.user import router as userrouter
from routers.authentication import router as loginroueter


models.Base.metadata.create_all(engine) #this will create a table mapped to models file
app= FastAPI()

app.include_router(blogrouter) # register the routes from blog route
app.include_router(userrouter) # register the user routes from user route
app.include_router(loginroueter) # register the login routes from authentication route
