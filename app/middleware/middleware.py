from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from starlette.responses import Response, JSONResponse
from fastapi.responses import RedirectResponse
import app.database.sql_executer as db

class Middleware(BaseHTTPMiddleware):
    """
    middleware for app
    1. checks session validation
    """
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        
        # check session validation
        route = str(request.url).replace(str(request.base_url), '')
        try:
            uid = request.headers['uid']
            sessionID = request.headers['sessionID']
            # print(f"Header : uid: {uid}, sessionID: {sessionID}")
        except Exception as e:
            print(f"Header error. {e}")
            # TODO : delete this part and send error log after testing
            uid = 1
            sessionID = 1

            # return JSONResponse(status_code=400, content= "Header Error")

        if(route[0:10] == "auth/login" or route == "docs" or route == "openapi.json"):
            # do nothing
            print("session check pass route")

        else :
            if not await session_check(uid, sessionID):
                # wrong session id
                res = JSONResponse(status_code= 440, content= f"Session Expired",)
                return res
        
        # 실행
        try:
            res: Response = await call_next(request)
        except Exception as e:
            res = JSONResponse(status_code= 500, content= f"Internal Server Error {e}",)

        return res


async def session_check(uid: int, sessionID: int) -> bool:
    # check session validation
    sql = """
            select *
            from wdygo.session
            where session_id = %s and uid = %s
        """
    values = (sessionID, uid)

    result = await db.sql_read(sql, values)

    if len(result) > 0:
        res = result[0]
        if res["expire_date"]>datetime.now():
            await refresh_session(sessionID)
            return True


    # if result["expire_date"] > datetime.now():

    return False

async def refresh_session(sessionID: int):
    sql = """
            UPDATE wdygo.session
            SET expire_date = %s
            WHERE session_id = %s
        """
    ten_minute_from_now = datetime.now() + timedelta(minutes = 10)
    values = (ten_minute_from_now, sessionID)

    await db.sql_write(sql, values)
