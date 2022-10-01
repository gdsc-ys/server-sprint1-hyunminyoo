import aiomysql
import app.main as main


# for db write (insert, update, delete)
async def sql_write(sql, values):
    pool = main.app.state.db_pool
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            try:
                await cur.execute(sql, values)
                result = None
                # update 영향 받은 row 수
                rowcount = cur.rowcount
                if rowcount:
                    result = rowcount

                # insert 한 경우 primary key id
                last_id = cur.lastrowid
                if last_id:
                    result = last_id

                # await conn.commit()
                return result

            except Exception as e:
                print(f"error happened in sql_write : {e}")
                return e


async def sql_read(sql, values) -> list:
    pool = main.app.state.db_pool
    async with pool.acquire() as conn:
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, values)
                result = await cur.fetchall()

                # commit을 안하면 캐싱 되서 업데이트 된 값을 안가져오고 예젼 값을 가져온다.
                # https://stackoverflow.com/questions/21974169/how-to-disable-query-cache-with-mysql-connector
                # 2020-03-24 20:00:00 -> autocommit 켜놔서 이제 commit 호출 안해도 됨.
                # await conn.commit()

                return result
        except Exception as e:
            print(f"error happened in __sql_read : {e}")
            return e
