import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends, Header, HTTPException

app = FastAPI()

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"hello~{name}"}


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str

@app.post("/register")
def register(data: RegisterRequest):
    return {"message": f"{data.username}注册成功"}


def check_token(token: str = Header()):
    if token != "abc123":
        raise HTTPException(status_code=401, detail="未登录")
    return token


@app.get("/profile")
def profile(token: str = Depends(check_token)):
    return {"message": "获取个人信息"}


@app.middleware("http")
async def add_timer(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} 耗时 {duration:.3f}s")
    return response





































