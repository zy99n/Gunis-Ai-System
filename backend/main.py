import structlog
from fastapi import FastAPI
from common.config.settings import settings
from common.middleware.cors_middleware import setup_cors
from common.middleware.logging_middleware import LoggingMiddleware
from common.middleware.jwt_middleware import JWTAuthenticationMiddleware
from apps.auth.api import router as auth_router
from apps.organization.api import router as organization_router
from apps.model.api import router as model_router
from apps.nl2sql.api import router as nl2sql_router
from apps.skill.api import router as skill_router
from apps.employee.api import router as employee_router
from apps.data.api import router as data_router
from apps.admin.api import router as admin_router
from apps.im.api import router as im_router

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
app.include_router(organization_router, prefix="/api/organization", tags=["组织管理"])
app.include_router(model_router, prefix="/api/model", tags=["模型管理"])
app.include_router(nl2sql_router, prefix="/api/nl2sql", tags=["智能问数"])
app.include_router(skill_router, prefix="/api/skill", tags=["AI技能"])
app.include_router(employee_router, prefix="/api/employee", tags=["数字员工"])
app.include_router(data_router, prefix="/api/data", tags=["数据采集"])
app.include_router(admin_router, prefix="/api/admin", tags=["系统管理"])
app.include_router(im_router, prefix="/api/im", tags=["即时通讯"])

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