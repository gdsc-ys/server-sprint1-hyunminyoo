from datetime import datetime
from fastapi import FastAPI, Depends
from starlette.responses import Response
from app.middleware.middleware import Middleware
from app.routes import index, auth, user, favorite
from app.common.config import conf
import aiomysql
from starlette_context import context
import orjson
from json import JSONDecodeError
from starlette.requests import Request
import aioredis
from typing import AsyncIterator


conf = conf()

app = FastAPI()

# Request, Response 확인(middleware/* 이후에 처리됨)
async def request_body(request: Request):
    try:
        context.update(request_body=orjson.loads(await request.body()))
    except JSONDecodeError:
        pass


#define routers
app.include_router(index.router)
app.include_router(auth.router, tags=["Auth"])
app.include_router(user.router, tags=["User"])
app.include_router(favorite.router, tags=["Favorite"])

# add middleware
@app.on_event("startup")
async def add_middleware():
    """
    Add middleware to the app
    """
    app.add_middleware(Middleware)

# connect DB
@app.on_event("startup")
async def connect_DB():
    app.state.db_pool = await aiomysql.create_pool(
        host=conf.DB_HOST, port=conf.DB_PORT,
        user=conf.DB_USER, password=conf.DB_PW,
        db='mysql', autocommit=True, minsize=20, maxsize=40
    )

# connect redis
@app.on_event("startup")
async def init_redis_pool():
    app.state.redis = aioredis.from_url(
        f'redis://{conf.REDIS_HOST}:{conf.REDIS_PORT}',
        decode_responses=True
    )
