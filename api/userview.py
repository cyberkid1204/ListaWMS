# !/usr/bin/env python
# -*-   coding:utf-8   -*-
# Author     ：NanZhou
# version    ：python 3.11
# =============================================
import hashlib
import time
from uuid import UUID, uuid4
from models.user import Users, Roles
from Utils.cookie import backend, SessionData, cookie, InDatabaseBackend
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi import requests, HTTPException, FastAPI, Response, Depends
from templates import template
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

user_router = APIRouter(prefix="/user", tags=["user"])


class User(BaseModel):
    username: str
    password: str
    email: str


class Role(BaseModel):
    role_name: str


async def get_current_user(session_id):
    # 获取当前用户
    return await Users.filter(session_id=session_id).first()


@user_router.post("/register/")
# 用户注册
async def register_user(user: User, response: Response):
    username = await Users.filter(username=user.username).first()
    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    hs_password = hashlib.md5(user.password.encode())
    session_id = uuid4()
    user = await Users.create(
        username=user.username,
        password=hs_password.hexdigest(),
        email=user.email,
        session_id=session_id,
    )
    User = await get_current_user(session_id)
    role = await Roles.create(role_name="user", users_id=User.id)
    SessionData(username=user.username)
    await InDatabaseBackend.update(user.username, session_id)
    # cookie.attach_to_response(response, session_id)
    response.set_cookie(key="session_id", value=str(session_id))
    return {"code": status.HTTP_200_OK, "message": "注册成功"}


@user_router.post("/login/", name="login")
# 用户登录
async def login_user(request: requests.Request, user: User, response: Response):
    hs_password = hashlib.md5(user.password.encode())
    user = await Users.filter(
        username=user.username, password=hs_password.hexdigest()
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    session_id = uuid4()
    await InDatabaseBackend.update(user.username, session_id)
    response.set_cookie(key="session_id", value=str(session_id))
    return template.TemplateResponse(
        "page-login.html", {"request": request, "code": 200, "message": "登录成功"}
    )


@user_router.get("/whoami")
async def whoami(self, session_data: SessionData = Depends(cookie)):
    # print(session_data.username)
    return session_data


@user_router.get("/login/")
async def login_page(request: requests.Request, response: Response):
    if not request.cookies:
        return template.TemplateResponse("page-login.html", {"request": request})
    # cookie.delete_from_response(response)
    response.delete_cookie(key="session_id")
    return template.TemplateResponse("page-login.html", {"request": request})
    # return {"code": 200, "message": "注册成功"}


@user_router.get("/logout/")
# 用户登出
async def logout_user(response: Response):
    # await InDatabaseBackend.delete(session_id)
    # cookie.delete_from_response(response)
    response.delete_cookie(key="session_id")

    # re_guiding = RedirectResponse(url='../login', status_code=status.HTTP_302_FOUND)
    return {"code": status.HTTP_200_OK, "message": "退出登录成功"}


@user_router.get("/")
async def get_all_user(request: requests.Request) -> JSONResponse:
    all_user = await Users.all()
    return {"all_user": all_user}


@user_router.get("/roles/")
# 获取用户角色
async def user_roles(request: requests.Request):
    all_roles = await Roles.all()
    return {"all_roles": all_roles}


@user_router.post("/roles/")
# 创建用户角色
async def create_user_roles(
    request: requests.Request,
    role: Role,
    current_user: User = Depends(get_current_user),
):
    role = await Roles.create(role=role.role_name, user_id=current_user.id)
    return {"code": status.HTTP_200_OK, "message": "创建用户角色成功"}


@user_router.put("/roles/")
# 更新用户角色
async def update_user_roles(
    request: requests.Request,
    role: Role,
    current_user: User = Depends(get_current_user),
):
    role = await Roles.create(role=role.role_name, user_id=current_user.id)
    return template.TemplateResponse(
        "page-roles.html", {"request": request, "role": role}
    )


@user_router.delete("/roles/")
# 删除用户角色
async def delete_user_roles(
    request: requests.Request,
    role: Role,
    current_user: User = Depends(get_current_user),
):
    role = await Roles.delete(role=role.role_name, user_id=current_user.id)
    return template.TemplateResponse(
        "page-roles.html", {"request": request, "role": role}
    )
