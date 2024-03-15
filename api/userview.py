# !/usr/bin/env python
# -*-   coding:utf-8   -*-
# Author     ：NanZhou
# version    ：python 3.11
# =============================================
import hashlib
import time
from uuid import UUID, uuid4
from models.user import Users
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


@user_router.post("/register/")
# 用户注册
async def register_user(user: User, response: Response):
    username = await Users.filter(username=user.username).first()
    if username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hs_password = hashlib.md5(user.password.encode())
    session_id = uuid4()
    user = await Users.create(username=user.username, password=hs_password.hexdigest(), email=user.email,
                              session_id=session_id)
    import logging

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info(f"用户注册 - 用户名: {user.username}, 邮箱: {user.email}")
    SessionData(username=user.username)
    await InDatabaseBackend.update(user.username, session_id)
    # cookie.attach_to_response(response, session_id)
    response.set_cookie(key="session_id", value=str(session_id))
    return {"code": status.HTTP_200_OK, "message": "注册成功"}


@user_router.post("/login/", name="login")
# 用户登录
async def login_user(request: requests.Request, user: User, response: Response):
    hs_password = hashlib.md5(user.password.encode())
    user = await Users.filter(username=user.username, password=hs_password.hexdigest()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    session_id = uuid4()
    await InDatabaseBackend.update(user.username, session_id)
    response.set_cookie(key="session_id", value=str(session_id))
    return template.TemplateResponse("page-login.html", {"request": request, "code": 200, "message": "登录成功"})


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


@user_router.get("/whoami")
async def whoami(session_data: SessionData = Depends(cookie)):
    # print(session_data.username)
    return session_data


@user_router.get("/")
async def get_all_user(request: requests.Request):
    """
    get all user
    """
    print(1234243)
    # template = Jinja2Templates(directory="templates")
    all_user = await Users.all()
    print(all_user[0].username)
    return template.TemplateResponse("page-register.html", {"request": request, "all_user": all_user})
