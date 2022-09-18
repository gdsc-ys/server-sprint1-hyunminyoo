from datetime import datetime
from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()

@router.get("/")
async def index():
    """
    root API
    return current UTC time
    """
    current_time = datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")        