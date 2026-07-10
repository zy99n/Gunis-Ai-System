# backend/common/security/password.py
import bcrypt
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_password_hash(password: str) -> str:
    """
    使用 bcrypt 加密密码
    自动截断超过72字节的密码
    """
    if not password:
        raise ValueError("密码不能为空")
    
    # bcrypt 限制密码长度为72字节
    # 如果密码超过72字节，截断到72字节
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        logger.warning(f"密码长度 {len(password_bytes)} 超过72字节，将进行截断")
        password_bytes = password_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        # 截断密码到72字节
        password_bytes = plain_password.encode('utf-8')[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except ValueError as e:
        logger.error(f"密码验证失败: {e}")
        return False
    except Exception as e:
        logger.error(f"密码验证异常: {e}")
        return False