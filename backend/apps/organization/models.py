from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
from apps.auth.models import User

class Department(BaseModel):
    """部门模型"""
    __tablename__ = "departments"
    
    name = Column(String(100), nullable=False, comment="部门名称")
    parent_id = Column(Integer, ForeignKey("departments.id"), nullable=True, comment="父部门ID")
    sort_order = Column(Integer, default=0, comment="排序")
    description = Column(Text, nullable=True, comment="部门描述")
    
    children = relationship("Department", back_populates="parent", remote_side="Department.id")
    parent = relationship("Department", back_populates="children")
    
    def __repr__(self):
        return f"<Department(name={self.name}, id={self.id})>"

class UserDepartment(BaseModel):
    """用户-部门关联模型"""
    __tablename__ = "user_department"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, comment="部门ID")
    is_primary = Column(Boolean, default=True, comment="是否为主部门")
    
    user = relationship("User", backref="department_relations")
    department = relationship("Department", backref="user_relations")
    
    def __repr__(self):
        return f"<UserDepartment(user_id={self.user_id}, department_id={self.department_id})>"