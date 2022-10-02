from typing import List
from urllib import response
from app.models.user_model import GetNickResp, PutNickReq
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
import app.database.sql_executer as db

router = APIRouter(prefix='/user')


@router.get('/nickname', response_model=GetNickResp)
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
        return ORJSONResponse(status_code=200, content= result[0]) 
    else :
        return HTTPException(status_code=500, detail=str(result))


@router.put('/nickname')
async def modify_nickname(uid: int, nickname: str):
    sql = """
            UPDATE wdygo.user_info
            SET nickname = %s
            WHERE uid = %s
        """
    
    values = (nickname, uid)


    result = await db.sql_write(sql, values)

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))

    return ORJSONResponse(status_code=200, content= "Success") 


