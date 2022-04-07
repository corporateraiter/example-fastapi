
from fastapi import FastAPI
from . import models         #https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables
from .database import engine  #https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables
from .routers import post, user, auth, vote
#from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#from fastapi documentation for sqlalchemy under main "create the database tables"
#this line below is optional given alembic 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#name and location of the webapp that is accessing the api (or ["*"]) for open/public
#origins = ["https://www.alienag.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
           
#send posts and user requests to router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API, bruh!"}





