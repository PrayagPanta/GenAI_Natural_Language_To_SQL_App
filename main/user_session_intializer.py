import aiosqlite
from datetime import datetime, timedelta

async def init_db():
    async with aiosqlite.connect("user_sessions.db") as conn:
        await conn.execute("DROP TABLE IF EXISTS user_sessions")
        await conn.execute("""
            CREATE TABLE user_sessions (
                session_id TEXT PRIMARY KEY,
                user_query TEXT,
                generated_sql TEXT,
                current_page INTEGER,
                last_accessed TIMESTAMP,
                user_rating INTEGER
            )
        """)
        await conn.commit()

async def get_session_data(session_id: str):
    async with aiosqlite.connect("user_sessions.db") as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("""
            SELECT * FROM user_sessions 
            WHERE session_id = ? AND last_accessed > ?
        """, (session_id, datetime.now() - timedelta(hours=1)))
        return await cursor.fetchone()

async def set_session_data(session_id: str, user_query: str, generated_sql: str, current_page: int):
    async with aiosqlite.connect("user_sessions.db") as conn:
        await conn.execute("""
            INSERT INTO user_sessions (session_id, user_query, generated_sql, current_page, last_accessed)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                user_query = excluded.user_query,
                generated_sql = excluded.generated_sql,
                current_page = excluded.current_page,
                last_accessed = excluded.last_accessed
        """, (session_id, user_query, generated_sql, current_page, datetime.now()))
        await conn.commit()

async def update_user_rating(session_id: str, rating: int):
    async with aiosqlite.connect("user_sessions.db") as conn:
        await conn.execute("""
            UPDATE user_sessions
            SET user_rating = ?, last_accessed = ?
            WHERE session_id = ?
        """, (rating, datetime.now(), session_id))
        await conn.commit()

async def cleanup_old_sessions():
    async with aiosqlite.connect("user_sessions.db") as conn:
        await conn.execute("""
            DELETE FROM user_sessions 
            WHERE last_accessed < ?
        """, (datetime.now() - timedelta(hours=1),))
        await conn.commit()