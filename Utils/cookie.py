# !/usr/bin/env python
# -*-   coding:utf-8   -*-
# Author     ：NanZhou
# version    ：python 3.11
# =============================================
from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4
from models.user import Users
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="ListaWMSisYourBestChoice",
    cookie_params=cookie_params,
)

backend = InMemoryBackend[UUID, SessionData]()


class InDatabaseBackend:
    def __init__(self):
        self.username = ''
        self.sessions_id = ''
        self.session_data = ''

    @staticmethod
    async def update(username, session_id):
        try:
            await Users.filter(username=username).update(session_id=session_id)
            return username, session_id
        except Exception as e:
            return str(e)

    @staticmethod
    async def read(username, session_id):
        try:
            user = await Users.filter(username=username, session_id=session_id).first()
            return user.username
        except Exception as e:
            return str(e)

    @staticmethod
    async def delete(session_id):
        try:
            await Users.filter(session_id=session_id).update(session_id='')
            return session_id
        except Exception as e:
            return str(e)


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

app = FastAPI()


@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):
    session = uuid4()
    print(session)
    data = SessionData(username=name)

    result = await backend.create(session, data)
    print(result)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
