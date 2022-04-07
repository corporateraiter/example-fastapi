from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')  #pass in end end point of login


#SECRET_KEY
#Algorithm
#expiration time of token (how long user stays logged in)

SECRET_KEY = settings.secret_key   #"4hslkdj38938dhsl301ablsyeleny3il298374765p"
ALGORITHM = settings.algorithm     #"HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes   #60

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #add an expiration time key pair to the to_encode dict object
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        #if not id:
        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oath2_scheme),
    db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail = f"Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user






