import re
from typing import List, Tuple
import aiosqlite
from fastapi import Depends


# Path to the SQLite database for flight data
DB_PATH = "../cleaned_flights.db"

def get_db_connection(db_path: str = DB_PATH) -> aiosqlite.Connection:
    """Provides a database connection for dependency injection."""
    return aiosqlite.connect(db_path)

async def execute_sql_query(query: str, connection: aiosqlite.Connection = Depends(get_db_connection)) -> Tuple[List[dict], List[str]]:
    """Executes the SQL query against the SQLite database and returns results."""
    async with connection.execute(query) as cursor:
        rows = await cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        return rows, columns

def get_cleaned_query(gemini_response: dict) -> str:
    """Cleans and formats the SQL query from the Gemini response."""
    raw_text = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
    if "```" in raw_text:
        match = re.search(r"```(?:sqlite)?\s*(.*?)\s*```", raw_text, flags=re.DOTALL)
        if match:
            raw_text = match.group(1)
    clean_query = re.sub(r'\s+', ' ', raw_text).strip()
    clean_query = re.sub(r'\bsqlite\b', '', clean_query, flags=re.IGNORECASE)
    if not clean_query.endswith(";"):
        clean_query += ";"
    return clean_query


def add_pagination_to_query(query: str, page: int, page_size: int) -> str:
    """Adds pagination (LIMIT and OFFSET) to the SQL query."""
    if query.strip().lower().startswith("select"):
        query = re.sub(r'\blimit\s+\d+\s+offset\s+\d+\s*;?$', '', query, flags=re.IGNORECASE)
        query = query.strip().rstrip(";")
        total_limit = page * page_size
        return f"{query} LIMIT {total_limit} OFFSET 0;"
    return query

