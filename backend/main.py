import structlog
from fastapi import FastAPI
from common.config.settings import settings
from common.middleware.cors_middleware import setup_cors
from common.middleware.logging_middleware import LoggingMiddleware
from common.middleware.jwt_middleware import JWTAuthenticationMiddleware
from apps.auth.api import router as auth_router

# 配置日志
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="企业智能协同平台API文档",
    debug=settings.DEBUG
)

# 配置中间件
setup_cors(app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(JWTAuthenticationMiddleware)

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])

@app.get("/")
async def root():
    return {
        "message": f"欢迎使用{settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )