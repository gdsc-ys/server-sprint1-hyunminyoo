from datetime import datetime
from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()


@app.get("/")
async def root():
    """
    root API
    return current UTC time
    """
    current_time = datetime.utcnow()
    return Response(f"UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}")        