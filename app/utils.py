from passlib.context import CryptContext

#from fastapi documentation https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=password+hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    

