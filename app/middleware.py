import os
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWKError, JWTError
from fastapi import FastAPI

JWT_SECRET=os.getenv("JWT_SECRET")

def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):

        if request.url.path in ["/"]:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing token"})

        try:
            token = auth.split()[1]
            request.state.user = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        except ExpiredSignatureError as e:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except Exception as e:
            print(e)    
            return JSONResponse(status_code=401, content={"detail": f"ERROR: {e}"})
                  
        return await call_next(request)