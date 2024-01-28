from typing import Optional

import aiosqlite

from data.config import DATABASE_NAME


class DB:
    database_name = DATABASE_NAME

    @classmethod
    async def setup_database(cls):
        async with aiosqlite.connect(cls.database_name) as conn:
            cursor = await conn.cursor()

            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages(
                    sender_id BIGINT PRIMARY KEY,
                    text TEXT,
                    keyboard TEXT
                )
            """
            )

            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    sender_id BIGINT PRIMARY KEY,
                    user_id BIGINT
                )
            """
            )

            await conn.commit()

    @classmethod
    async def select_one(cls, query: str, params: Optional[tuple] = None) -> tuple:
        async with aiosqlite.connect(cls.database_name) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchone()

    @classmethod
    async def select_all(cls, query: str, params: Optional[tuple] = None) -> list[tuple]:
        async with aiosqlite.connect(cls.database_name) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchall()

    @classmethod
    async def update(cls, query: str, params: Optional[tuple] = None) -> bool:
        async with aiosqlite.connect(cls.database_name) as db:
            await db.execute(query, params)
            await db.commit()
            return True

    @classmethod
    async def insert(cls, query: str, params: Optional[tuple] = None) -> bool:
        async with aiosqlite.connect(cls.database_name) as db:
            await db.execute(query, params)
            await db.commit()
            return True

    @classmethod
    async def delete(cls, query: str, params: Optional[tuple] = None) -> bool:
        async with aiosqlite.connect(cls.database_name) as db:
            await db.execute(query, params)
            await db.commit()
            return True

# async def update_last_message(sender_id: str, text: str, keyboard: Optional[Keyboard] = None):
#     keyboard_data = None
#     if keyboard:
#         keyboard_data = json.dumps(keyboard.to_dict())
#
#     await DB.insert(
#         """INSERT OR REPLACE INTO messages VALUES (?,?,?)""", (sender_id, text, keyboard_data)
#     )
