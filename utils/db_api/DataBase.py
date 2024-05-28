import asyncpg
from asyncpg import create_pool, pool, Connection
from data import config


class Database:
    #     self.conn = await asyncpg.connect(
    #         user=config.DB_USER,
    #         password=config.DB_PASS,
    #         host=config.DB_HOST,
    #         database=config.DATABASE
    #     )
        # self.pool = await create_pool(
        #     user=config.DB_USER,
        #     password=config.DB_PASS,
        #     host=config.DB_HOST,
        #     database=config.DATABASE
        # )

    async def execute(self, sql: str, params: tuple=None, fetchone: bool=False,
                      fetchall: bool=False, execute: bool=False):
        connection = await asyncpg.connect(
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME,
            host=config.DB_HOST
        )
        connection: Connection
        data = None
        async with connection.transaction() as connection:
            if execute:
                data = await connection.execute(sql, params)
            if fetchone:
                data = await connection.fetchval(sql, params)
            if fetchall:
                data = await connection.fetch(sql, params)
        return data

    async def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS telegram_users(id INT PRIMARY KEY, full_name TEXT, group_ TEXT, language TEXT)"
        await self.execute(sql, execute=True)

    async def insert_into_table(self, table: str, values: tuple):
        if table == "Users":
            parameters = "(id, full_name, group, language)"
            command = f"INSERT INTO Users{parameters} VALUES ($1, $2, $3, $4)"
            await self.execute(sql=command, params=values)


        # async with self.pool.acquire() as connection:
        #     connection: Connection
        #     data = None
        #     async with connection.transaction():
        #         if execute:
        #             data = await connection.execute(sql, params)
        #         if fetchone:
        #             data = await connection.fetchval()
