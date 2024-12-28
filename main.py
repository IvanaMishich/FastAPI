from fastapi import FastAPI, Cookie, Response, Header, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Feedback, User, User2
from typing import Annotated

app = FastAPI()
security = HTTPBasic()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return fake_users.get(user_id, {"error": "User not found"})


@app.get("/users/")
async def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])

data = []


@app.post("/feedback")
async def feedbacks(f: Feedback):
    data.append(f)
    return {"message": f"Thank you, {f.name}!"}


@app.post("/create_user")
async def creating(user: User) -> User:
    return user

products_list = [{
    "product_id": 1,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}, {
    "product_id": 2,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}, {
    "product_id": 3,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}]


@app.get("/product/{product_id}")
async def product(product_id: int):
    return [pr for pr in products_list if pr.get("product_id") == product_id]


@app.get("/products/search")
async def search(keyword: str, category: str = None, limit: int = 10):
    if category:
        return [pr for pr in products_list if (keyword in pr.get("name")) and (category == pr.get("category"))][:limit]
    else:
        return [pr for pr in products_list if keyword in pr.get("name")][:limit]


#Устанавливаем Cookie
sessions = {}
example = [{
  "username": "user123",
  "password": "password123"
}]


@app.post("/login")
async def login(user: User2, response: Response):
    for n in example:
        if user.username == n.get("username") and user.password == n.get("password"):
            session_token = "ex2am1pl8e"
            sessions[session_token] = user
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            return {"message": "куки установлены"}
    return {"message": "Invalid username or password"}


@app.get("/user")
async def about(session_token = Cookie(default=None)):
    user = sessions.get(session_token)
    if user:
        return user.dict()
    return {"message": "Unauthorized"}


#Извлекаем заголовки
@app.get("/headers")
async def heads(user_agent: Annotated[ str | None, Header()] = None,
                accept_language: Annotated[ str | None, Header()] = None):
    if user_agent and accept_language:
        return {
            "User-Agent": user_agent,
            "Accept-Language": accept_language
        }
    else:
        raise HTTPException(status_code=400, detail="Missing required headers")

#Аутентификация
USER_DATA = [User2(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]

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
def get_protected_resource(user: User2 = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}
