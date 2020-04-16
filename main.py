from datetime import datetime, timedelta
from pymongo import MongoClient
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBasic,HTTPBasicCredentials
from jwt import PyJWTError
from passlib.context import CryptContext
from starlette.responses import RedirectResponse
from pydantic import BaseModel,EmailStr
from fastapi.encoders import jsonable_encoder


# mongodb configuration
client = MongoClient("mongodb://127.0.0.1:27017")
users_db=client["userdatabase"]
Users_Collection=users_db["users"]
massage_db=client["massageDatabase"]
massage_collection=massage_db["massages"]

# Oauth2 security secret key and algorithm
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
active_user=[]
active_user_token=[]


class Massage(BaseModel):
    massage: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    disabled: bool = None


class UserInDB(User):
    password: str



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

security = HTTPBasic()

#this function varifies the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# function to get hashed passwored 
def get_password_hash(password):
    return pwd_context.hash(password)

# funtion to query user in DB coresponding to given username
def get_user(Users_Collection, username: str):
    found_user=Users_Collection.find({'username':username})
    for user in found_user:
        user_dict = user
        return UserInDB(**user_dict)
    

# function to authenticate user by calling get_user function and varify_password function
def authenticate_user(Users_Collection, username: str, password: str):
    user = get_user(Users_Collection, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# function to create access token
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# funtion to get the curren active token by using token stored in cookie
async def get_current_user():
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if(not active_user_token):
            raise credentials_exception
        token=active_user_token[-1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user(Users_Collection, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# wellcome route
@app.get("/")
def wellocme():
    return {"mag":"Hello and wellcome plase goto /login to login"}

#login route
@app.get("/login")
def login_user(credentials: HTTPBasicCredentials = Depends(security)):
    print(credentials)
    user = authenticate_user(Users_Collection, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    active_user.append(user.username)
    active_user_token.append(access_token)
    response = RedirectResponse(url="/users/me")

    token = jsonable_encoder(access_token)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        domain="localtest.me",
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


# current active user route
@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    user_detail=dict()
    user_detail["full_name"]=current_user.full_name
    user_detail["username"]=current_user.username
    user_detail["email"]=current_user.email
    return user_detail

# route to get all the massages curresponding to current active user
@app.get("/users/me/massages/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    current_username={"username":current_user.username}
    current_user_in_db=Users_Collection.find(current_username)
    for user in current_user_in_db:
        current_id={"_id":str(user["_id"])}
    user_massages=massage_collection.find(current_id)
    for massage in user_massages:
        return massage["massages"]
    return {"Not Authenticated"}


# signup route
@app.post("/signup")
async def new_user(user:User):
    current_passworld=user.password
    hashed_password=get_password_hash(current_passworld)
    user.password=hashed_password
    current_email={'email':user.email}
    current_username={"username":user.username}
    auser=dict()
    auser['full_name']=user.full_name
    auser['email']=user.email
    auser['password']=user.password
    auser['username']=user.username

    current_user=Users_Collection.find(current_email)
    for x in current_user:
        return {"email already exists"}
    current_user=Users_Collection.find(current_username)
    for x in current_user:
        return {"username already exists"}

    new_user=Users_Collection.insert_one(auser)
    current_user=Users_Collection.find(current_email)
    for use in current_user:
        return {"id":str(use["_id"])}
    
# route to receive massage
@app.post("/users/me/sendmassage")
async def received_massage(massage:Massage,current_user: User = Depends(get_current_active_user)):
    current_massage={'massage':massage.massage}
    current_username={"username":current_user.username}
    current_user_in_db=Users_Collection.find(current_username)
    for user in current_user_in_db:
        current_id={"_id":str(user["_id"])}
    user_massages=massage_collection.find(current_id)
    for massage in user_massages:
        massage_collection.update(current_id,{"$push":{"massages": current_massage}})
        return {"massage has been saved"}
    massage_collection.insert({"_id":current_id["_id"],"massages":[current_massage]})
    return {"Your first massage has been saved"}