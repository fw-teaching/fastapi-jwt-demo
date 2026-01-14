import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from app.middleware import register_middleware

app = FastAPI()
register_middleware(app)

@app.get("/")
def read_root():
    return { "msg": "Open endpoint" }

@app.get("/protected")
def protected(request: Request):
    return { "msg": "For authorized users only", "authorizedUser": request.state.user }



