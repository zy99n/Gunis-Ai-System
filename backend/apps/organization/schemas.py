from pydantic import BaseModel, Field
from typing import Optional, List

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="部门名称")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    sort_order: Optional[int] = Field(0, description="排序")
    description: Optional[str] = Field(None, description="部门描述")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentTree(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    sort_order: int
    description: Optional[str]
    children: List["DepartmentTree"] = []
    
    class Config:
        from_attributes = True

class DepartmentList(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    sort_order: int
    description: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class UserDepartmentCreate(BaseModel):
    user_id: int = Field(..., description="用户ID")
    department_id: int = Field(..., description="部门ID")
    is_primary: Optional[bool] = Field(True, description="是否为主部门")

class UserDepartmentUpdate(BaseModel):
    is_primary: Optional[bool] = Field(None, description="是否为主部门")

class UserDepartmentResponse(BaseModel):
    id: int
    user_id: int
    department_id: int
    is_primary: bool
    department_name: Optional[str] = None
    
    class Config:
        from_attributes = True