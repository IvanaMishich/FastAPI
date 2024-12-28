import jwt
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from models import User3

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "123QWE456RT"
ALGORITHM = "HS256"

USERS_DATA = [
    {"username": "admin", "password": "adminpass", "role": "admin"}
]

permissions = [
    {"ADMIN": "create, read, update, delete"},
    {"USER": "read, update"},
    {"GUEST": "read"}
]


def create_jwt(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_jwt(token: str = Depends(oauth2_scheme)):
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return data.get("sub")


def get_user(userdata: str):
    for u in USERS_DATA:
        if u.get("username") == userdata:
            return u
    return None


@app.post("/login")
def login(user: User3):
    for u in USERS_DATA:
        if u.get("username") == user.username and u.get("password") == user.password:
            return {"access_token": create_jwt({"sub": user.username}), "token_type": "bearer"}
    return {"error": "Invalid credentials"}


@app.get("/protected_resource")
def protected(userdata: str = Depends(get_user_from_jwt)):
    user = get_user(userdata)
    if user.get("role") == "admin":
        return user
    return {"error": "User doesn't have access rights"}
