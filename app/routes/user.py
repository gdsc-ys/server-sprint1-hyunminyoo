from typing import List
from urllib import response
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, ORJSONResponse
import app.database.sql_executer as db

router = APIRouter(prefix='/user')


@router.get('/nickname',
            #  response_class=ORJSONResponse,
            #  response_model=str,
            #  responses={500: {'model': rm.Update_user_appversion.Update_user_appversio500}},
            #  name='version20210902'
            )
async def get_nickname(uid: int):
    sql = """
            select nickname
            from wdygo.user_info
            where uid = %s
        """
    values = (uid)

    result = await db.sql_read(sql, values)

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))

    if len(result) > 0 :
        return result[0]
    else :
        return HTTPException(status_code=500, detail=str(result))


