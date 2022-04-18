from pydantic import BaseModel, Field
from .model import UserBase


class Token(BaseModel):
    access_token: str = Field(..., description='Token值')
    token_type: str = Field(..., description='Token类型')


# 创建账号需要验证的条件
class UserCreate(UserBase):
    confirm: str = Field(..., description='确认密码')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'username': 'guest',
                'nickname': '访客',
                'email': 'guest@example.com',
                'mobile': '10086',
                'password': '123456',
                'confirm': '123456',
                'avatar': 'https://img2.woyaogexing.com/2021/05/03/dfcfaaffa8ed4e1a819eba8c10b856d4!400x400.jpeg'
            }
        }


class UserSet(BaseModel):
    id: int = Field(..., description="用户id")
    nickname: str = Field(..., description="用户昵称")
    email: str = Field(..., description="用户邮箱")
    mobile: str = Field(..., description="用户手机号")


# 用户权限配置
class UserPerm(BaseModel):
    user: str = Field(..., description='用户名')
    model: str = Field(..., description='模块')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'user': 'zhangsan',
                'model': 'user',
                'act': 'add'
            }
        }


# 用户角色配置
class UserRole(BaseModel):
    user: str = Field(..., description='用户名')
    role: str = Field(..., description='角色')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'user': 'zhangsan',
                'role': 'guest'
            }
        }
