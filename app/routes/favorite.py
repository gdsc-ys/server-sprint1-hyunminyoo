import json
from typing import List
from urllib import response
from app.models.favorite_model import GetFavoritesResp, PostFavoriteReq
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
import app.database.sql_executer as db
import app.main as main
import time

router = APIRouter(prefix='/favorite')


@router.get('/favorite')
async def get_favorites(uid: int):

    redis_start_time = time.time()

    redis_hit = await redis_get_favorite_by_uid(uid)

    redis_end_time = time.time()

    if len(redis_hit)>0:
        print(f"from redis time : {redis_end_time - redis_start_time}")
        return ORJSONResponse(status_code=200, content= {"favorite_list":redis_hit}) 

    else :
        db_start_time = time.time()
        sql = """
                SELECT id AS favorite_id, station_id
                FROM wdygo.favorites
                WHERE uid = %s
            """
        values = (uid)

        result = await db.sql_read(sql, values)

        db_end_time = time.time()

        print(f"from db time : {db_end_time - db_start_time}")

        if isinstance(result, Exception):
            raise HTTPException(status_code=500, detail=str(result))

        if len(result) > 0 :
            for i in range(0,len(result)):
                await redis_set_favorite(
                    result[i]["favorite_id"],
                    result[i]["station_id"],
                    uid
                )
            return ORJSONResponse(status_code=200, content= {"favorite_list":result})
        else :
            return ORJSONResponse(status_code=404, content="User Has No Favorites")


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

    await redis_set_favorite(result, req.station_id, req.uid)

    return ORJSONResponse(status_code=200, content= "Success") 

@router.post('/random_generate')
async def generate_random_values():

    for i in range(0, 100000):
        sql = """
                INSERT INTO wdygo.favorites
                (station_id, uid)
                VALUES (CEIL(RAND() * (10000)) , CEIL(RAND() * (10000)))
            """
        
        await db.sql_write(sql, ())

        print(f"{i} inputed")

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

    await redis_delete_favorite(favorite_id)

    return ORJSONResponse(status_code=200, content= "Success") 



async def redis_set_favorite(id:int, station_id:int, uid:int):
    redis = main.app.state.redis
    res = await redis.execute_command('JSON.SET', f'id:{id}', "$", f'{{"station_id":{station_id}, "uid":{uid}}}')

    return res

async def redis_delete_favorite(favorite_id: int):
    redis = main.app.state.redis
    res = await redis.execute_command('JSON.DEL', f'id:{favorite_id}')

    return res


async def redis_get_favorite_by_uid(uid:int):
    redis = main.app.state.redis
    res = await redis.execute_command('FT.SEARCH', 'fvrIndex', f'@uid:[{uid} {uid}]')

    num_result = res[0]

    favorite_list = []
    for i in range(0,num_result):
        favorite_list.append({
            "favorite_id": int(res[2*i+1].split(":")[1]),
            "station_id": json.loads(res[2*i+2][1])["station_id"]
        })

    return favorite_list
    

	
