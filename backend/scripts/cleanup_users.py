import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from common.config.settings import settings
from common.security.password import get_password_hash


async def cleanup_and_create_admin():
    """清理用户表并创建新的管理员账号"""
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True  # 添加连接预检
    )
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # 1. 删除所有用户（谨慎操作）
            print("删除现有用户...")
            await session.execute(text("DELETE FROM users"))
            await session.commit()
            print("用户表已清空")
            
            # 2. 创建管理员用户
            print("创建管理员用户...")
            admin_password = "admin@1234"
            admin_hash = get_password_hash(admin_password)
            print(f"密码哈希: {admin_hash}")
            print(f"哈希长度: {len(admin_hash)}")
            
            # 使用原生 SQL 插入
            await session.execute(
                text("""
                    INSERT INTO users (
                        username, email, password_hash, nickname, 
                        is_active, is_admin, created_at, updated_at
                    ) VALUES (
                        :username, :email, :password_hash, :nickname,
                        :is_active, :is_admin, NOW(), NOW()
                    )
                """),
                {
                    "username": "admin",
                    "email": "admin@example.com",
                    "password_hash": admin_hash,
                    "nickname": "Administrator",
                    "is_active": True,
                    "is_admin": True
                }
            )
            await session.commit()
            print("管理员用户创建成功!")
            
            # 3. 验证创建结果
            result = await session.execute(
                text("SELECT username, password_hash, LENGTH(password_hash) as hash_len FROM users WHERE username = 'admin'")
            )
            row = result.fetchone()
            if row:
                print(f"\n验证结果:")
                print(f"用户名: {row[0]}")
                print(f"密码哈希: {row[1][:20]}...")  # 只显示前20个字符
                print(f"哈希长度: {row[2]} (应为60)")
            else:
                print("错误: 管理员用户创建失败")
                
        except Exception as e:
            print(f"错误: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(cleanup_and_create_admin())