from typing import List
from urllib import response
from app.models.favorite_model import GetFavoritesResp, PostFavoriteReq
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
import app.database.sql_executer as db

router = APIRouter(prefix='/favorite')


@router.get('/favorite', response_model=GetFavoritesResp)
async def get_favorites(uid: int):
    sql = """
            SELECT id AS favorite_id, station_id
            FROM wdygo.favorites
            WHERE uid = %s
        """
    values = (uid)

    result = await db.sql_read(sql, values)

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))

    if len(result) > 0 :
        return ORJSONResponse(status_code=200, content= {"favorite_list":result}) 
    else :
        return HTTPException(status_code=404, detail="User Has No Favorites")


@router.post('/favorite')
async def add_favorite(req: PostFavoriteReq):
    sql = """
            INSERT INTO wdygo.favorites
            (station_id, uid)
            VALUES (%s, %s)
        """
    
    values = (req.station_id, req.uid)

    result = await db.sql_write(sql, values)

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))

    return ORJSONResponse(status_code=200, content= "Success") 


@router.delete('/favorite')
async def delete_favorite(uid: int, favorite_id: int):
    sql = """
            DELETE FROM wdygo.favorites
            WHERE uid = %s and id = %s
        """
    
    values = (uid, favorite_id)

    result = await db.sql_write(sql, values)

    print(result)

    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))

    if result == None:
        return ORJSONResponse(status_code=404, content= "No Item to be deleted")

    return ORJSONResponse(status_code=200, content= "Success") 


