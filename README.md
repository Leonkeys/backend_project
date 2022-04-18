# FastAPI+MySQL+Tortoise-orm项目模板

## 功能
- JWT token 认证。
- 基于 casbin 的权限验证


## 权限控制
- 登录、注册及路由中含有openapi的接口不进行登录和权限认证
```python
# 重载了 FastAPI.OAuth2 模块进行登录认证，此模块可以在 API 文档界面进行统一登录认证
# 为了适配这个功能登录接口的返回数据未采用统一格式，使用的时候需要注意
class OAuth2CustomJwt(OAuth2):
    ......
    async def __call__(self, request: Request) -> Optional[str]:
        """
        除了开放API、登录、注册、WebSocket接口外，其他接口均需要登录验证
        """
        for url, op in settings.NO_VERIFY_URL.items():
            if op == 'eq' and url == request.url.path.lower():
                return None
            elif op == 'in' and url in request.url.path.lower():
                return None

        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        try:
            playload = jwt.decode(
                param,
                settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise custom_exc.TokenExpired()
        except (jwt.JWTError, ValidationError, AttributeError):
            raise custom_exc.TokenAuthError()

        username = playload.get('username')
        user = await get_user_by_name(username=username)
        if not user:
            raise AuthenticationError("认证失败")
```
- 全局登录认证（除以上接口外，其余接口均进行登录认证）

```python
app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        dependencies=[Depends(OAuth2CustomJwt(tokenUrl="/user/login"))]
    )
```
全局进行 Depends(OAuth2CustomJwt(tokenUrl="/user/login")) 依赖注入

- 接口权限认证

首先通过以下接口进行权限配置

![](https://tva1.sinaimg.cn/large/008i3skNly1gt9npof3euj31480brq4v.jpg)

在接口上添加 Depends(Authority('user,check')) 依赖注入来判断权限
```python
@router.get(
    "/info",
    summary="获取当前用户信息",
    name="获取当前用户信息",
    response_model=schema.UserOut,
    response_model_exclude_unset=True,
    dependencies=[Depends(Authority('user,check'))]
)
```

- 操作权限认证

在接口中进行特殊权限认证，只要使用check_authority函数判断即可，如果无权限会抛出异常
```python
await check_authority(f'{request.state.user.username},auth,add')
```

## 配置
- 修改 API 文档默认地址

为了通过权限认证，将 API 文档地址修改为包含 openapi 的 URL
```python
# 文档地址 默认为docs
DOCS_URL: str = "/openapi/docs"
# 文档关联请求数据接口
OPENAPI_URL: str = "/openapi/openapi.json"
# redoc 文档
REDOC_URL: Optional[str] = "/openapi/redoc"
```

- 超级管理员

设置用户的 is_super = 1，就表示超级管理员，超级管理员拥有所有权限，可以跳过权限认证
```python
class Authority:
    ......
    async def __call__(self, request: Request):
        """
        超级管理员不需要进行权限认证
        :param request:
        :return:
        """
        model, act = self.policy.split(',')
        e = await get_casbin()

        # 超级用户拥有所有权限
        if request.state.user.is_super:
            return

        if not await e.has_permission(request.state.user.username, model, act):
            raise AuthenticationError(err_desc=f'Permission denied: [{self.policy}]')
```

## 运行
```shell script
# 进入虚拟环境, 安装python环境。
pip install -r requestment.txt
# 执行命令，启动项目
python run.py
```

