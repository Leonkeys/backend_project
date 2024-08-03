import os
from typing import Optional, Dict
from pathlib import Path

from pydantic import BaseSettings


class APISettings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = False

    # 项目文档
    TITLE: str = "测试项目"
    DESCRIPTION: str = "大型项目框架"
    # 文档地址 默认为docs
    DOCS_URL: str = "/openapi/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/openapi/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/openapi/redoc"

    # token过期时间秒
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'a'

    # 项目根路径
    BASE_PATH: Path = Path(__file__).resolve().parent.parent

    # 权限控制配置
    CASBIN_MODEL_PATH: Path = BASE_PATH.joinpath('config/rbac_model.conf')

    # 数据库连接配置
    # postgres://postgres:qwerty123@localhost:5432/events
    DATABASE_URI = ""

    REDIS_CONFIG: Dict = {
        "host": "",
        "port": 6379,
        "username": "",
        "password": "",
        "decode_responses": True
    }

    # 数据库配置
    DATABASE_CONFIG: Dict = {
        'connections': {
            'default': DATABASE_URI
        },
        'apps': {
            'models': {
                # 设置key值“default”的数据库连接
                'default_connection': 'default',
                'models': ['apps.user.model', 'casbin_tortoise_adapter', "apps.menu.model", "apps.role.model"]
            }
        },
        "routers": ["db_router.Router"],
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }

    # 不需要登录认证的 API
    NO_VERIFY_URL: Dict = {
        "/": "eq",  # 根目录
        "openapi": "in",  # 开发 API
        "/auth/login": "in",  # 登录
        "/auth/register": "in",  # 注册
        "/ws/": "in",  # ws 服务不需要登录
        "/auth/sso": "in"
    }


settings = APISettings()
