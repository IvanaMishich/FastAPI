from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User2

app = FastAPI()
security = HTTPBasic()


#Аутентификация
USER_DATA = [User2(**{"username": "user1", "password": "pass1"}), User2(**{"username": "user2", "password": "pass2"})]

async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    def get_user_from_db(username: str):
        for user in USER_DATA:
            if user.username == username:
                return user
            return None
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@app.get("/protected_resource/")
async def get_protected_resource(user: User2 = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}

@app.get("/login")
async def login(user: User2 = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome ", "user_info": user}
