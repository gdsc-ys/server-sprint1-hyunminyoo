from datetime import datetime
from fastapi import FastAPI
from starlette.responses import Response

from app.routes import index, auth

app = FastAPI()

#define routers
app.include_router(index.router)
app.include_router(auth.router)