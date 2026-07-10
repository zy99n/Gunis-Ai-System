from fastapi.middleware.cors import CORSMiddleware
from common.config.settings import settings
from fastapi import FastAPI

def setup_cors(app: FastAPI):
    """配置CORS中间件"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )