from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from starlette.responses import Response, JSONResponse
from fastapi.responses import RedirectResponse

class Middleware(BaseHTTPMiddleware):
    """
    middleware for app
    1. checks session validation
    2. 
    """
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # check session validation
        route = str(request.url).replace(str(request.base_url), '')
        try:
            uid = request.headers['uid']
            sessionID = request.headers['sessionID']
            # print(f"Header : uid: {uid}, sessionID: {sessionID}")
        except Exception as e:
            print(f"Header : error. {e}")
            # TODO : delete this part and send error log after testing
            uid = ""
            sessionID = ""

            # return JSONResponse(status_code=400, content= "Header Error")

        if(route == "auth/login" or route == "docs" or route == "openapi.json"):
            # do nothing
            print("session check pass route")

        else :
            if not await session_check(uid=uid, sessionID=sessionID):
                # wrong session id
                res = RedirectResponse("/auth/login")
                return res
        
        
        # 실행
        try:
            res: Response = await call_next(request)
        except Exception as e:
            res = JSONResponse(status_code= 500, content= f"Internal Server Error {e}",)

        return res


async def session_check(uid: str, sessionID: str) -> bool:
    # compare with session data
    # TODO : check session validation
    return False