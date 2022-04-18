from pydantic import BaseModel, Field
from .model import RoleCreate


# 角色列表
class RoleList(RoleCreate):
    id: int = Field(..., description="主键")


# 角色权限
class RolePerm(BaseModel):
    role: str = Field(..., description='角色')
    model: str = Field(..., description='模块')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'role': 'guest',
                'model': 'auth',
                'act': 'add'
            }
        }


class SetRole(RoleCreate):
    id: int = Field(..., description="权限id")