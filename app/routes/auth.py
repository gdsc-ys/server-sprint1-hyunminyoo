from datetime import datetime
from app.models.auth_model import LoginReps
from fastapi import APIRouter
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
import app.database.sql_executer as db

USER_UNDEFINED = "user_validation_failed"

router = APIRouter(prefix="/auth")


@router.get("/login",
            response_model=LoginReps,
)
async def login(id: str, pw: str):
    """
    login api
    get user info and log user in.
    return uid and session id

    if login false, return 404 if user info is not in DB
    """
    # check if user is valid
    loginResult = await checkUserValid(id, pw)
    if loginResult == USER_UNDEFINED:
        return ORJSONResponse(status_code=404)

    sessionId = await issueSession(loginResult["uid"])

    return ORJSONResponse(status_code=200, content={"uid": loginResult["uid"], "sessionID": sessionId})

@router.get("/logout")
async def logout(uid: int, sessionID: int):
    """
    logout api
    make session invalid
    """

    sql = """
            UPDATE wdygo.session
            SET expire_date = "1980-01-01 00:00:00"
            WHERE session_id = %s and uid = %s
        """
    values = (sessionID, uid)

    await db.sql_write(sql, values)



async def checkUserValid(id:str, pw:str):
    sql = """
            select *
            from wdygo.user_info
            where id = %s and pw = %s
        """
    values = (id, pw)

    result = await db.sql_read(sql, values)

    if len(result)>0:
        return result[0]
    else :
        return USER_UNDEFINED

async def issueSession(uid: int):
    sql = """
            INSERT INTO wdygo.session
            (uid, expire_date) VALUES (%s, CURRENT_TIME + INTERVAL 10 MINUTE)
        """

    values = (uid)

    result = await db.sql_write(sql, values)

    return result