from datetime import datetime
from fastapi import FastAPI
from starlette.responses import Response
from app.middleware.middleware import Middleware
from app.routes import index, auth
from app.common.config import conf
import aiomysql

conf = conf()

app = FastAPI()

#define routers
app.include_router(index.router)
app.include_router(auth.router)

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