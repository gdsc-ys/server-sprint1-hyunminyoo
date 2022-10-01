from typing import List
from urllib import response

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, ORJSONResponse

import app.database.sql_executer as db

router = APIRouter(prefix='/user')

from pydantic.main import BaseModel

class TEST(BaseModel):
    a:int


@router.post('/favorites',
            #  response_class=ORJSONResponse,
            #  response_model=str,
            #  responses={500: {'model': rm.Update_user_appversion.Update_user_appversio500}},
            #  name='version20210902'
            )
async def favorites(req:TEST):
    result = await db.sql_write(
        """
            SHOW databases;
        """,
    )
    # result = await db.sql_master_write(
    #     """
    #         UPDATE Application.user_meta_info
    #         SET version=%s, update_date = NOW() 
    #         WHERE uid=%s
    #     """,
    #     (av, uid)
    # )
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))

    return 'Success'


