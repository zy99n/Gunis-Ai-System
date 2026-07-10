from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from common.security.jwt import decode_token

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    """JWT认证中间件"""
    
    # 不需要认证的路径
    EXCLUDE_PATHS = {
        "/",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/api/auth/register",
        "/api/auth/login",
    }
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in self.EXCLUDE_PATHS or path.startswith("/socket.io/"):
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            payload = decode_token(token)
            if payload:
                request.state.user_id = payload.get("user_id")
                request.state.username = payload.get("username")
        
        response = await call_next(request)
        return response