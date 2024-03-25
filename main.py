import uvicorn
from api.userview import user_router
from fastapi import FastAPI, requests, Depends
from config import TORTOISE_ORM
from Utils.cookie import backend, SessionData, cookie
from templates import template
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="ListaWMS", version="1.0.0", description="Warehouse Manage System")

# 注册路由
app.include_router(user_router)
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
# 注册tortoise
register_tortoise(app=app, config=TORTOISE_ORM)

origins = [
    "*",
    "http://localhost:63342",
    "http://localhost:8001",
]
# 跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/", name="index")
async def root(request: requests.Request):
    # 判断请求头里有没有cookie
    print(request.cookies)
    if not request.cookies:
        return template.TemplateResponse("page-register.html", {"request": request})
    return template.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard")
async def dash_board(request: requests.Request):
    return template.TemplateResponse("test.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=1)
