from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time as tm
import psycopg2
from psycopg2.extras import RealDictCursor
from . config import settings
#from .database import Base

#format of connection string we need to pass into sqlalchemy
#SQL_ALCHEMY_DATABASE_URL= 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"  
    #password  was 'Fuckyou1'

#lots of this is explained in the fastapi docs here: https://fastapi.tiangolo.com/tutorial/sql-databases/

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#from fastapi documentation for sqlalchemy under main "create the database tables" --
#moved to database.py and imported into main in order to keep main cleaner
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#try / catch block to attempt to connect to database

#put this in a while block to attempt reconnections -- it is for reference
# use if you want to us the postgres database relationship model with raw sql versus 
#sql alchemy which is being used now.

#while True:
#
#   try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', 
#            user='postgres', password='Fuckyou1', cursor_factory=RealDictCursor)  #pass in host, database, username, password
#        cursor = conn.cursor()
#        print("database connection was successful!")
#        break
#
 #   except Exception as error:
 #       print("database failed to connect")
 #       print("error was:", error)
  #      tm.sleep(5)        