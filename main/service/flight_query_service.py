import re
from typing import List, Tuple

import aiosqlite
from loguru import logger

from prompts.nlp_to_sql_prompt import get_prompt_to_correct_error
from service.gemini_service import make_http_request_to_gemini

# Path to the SQLite database for flight data
DB_PATH = "../cleaned_flights.db"


async def execute_sql_query(query: str) -> Tuple[List[dict], List[str]]:
    """Executes the SQL query against the SQLite database and returns results."""
    connection = await aiosqlite.connect(DB_PATH)
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
        offset = (page - 1) * page_size
        return f"{query} LIMIT {page_size} OFFSET {offset};"
    return query


async def execute_generated_query(base_sqlite_query: str, page: int, page_size: int, paginated_query: str,
                                  prompt: str) -> tuple:
    """Executes the generated query and returns columns with column names and subsequent data rows."""
    try:
        logger.info(f"Executing generated query :: {paginated_query}")
        rows, columns = await execute_sql_query(paginated_query)
    except Exception as sql_execution_exception:
        logger.error(f"Encountered error {sql_execution_exception} while executing the query. Attempting to generate "
                     f"corrected query again.")
        corrected_query = await correct_query_error(base_sqlite_query, prompt, sql_execution_exception)
        paginated_query = add_pagination_to_query(corrected_query, page, page_size)
        logger.info(f"Executing corrected query :: {paginated_query}")
        rows, columns = await execute_sql_query(paginated_query)
    return columns, rows


async def correct_query_error(base_sqlite_query: str, previous_prompt: str, sql_query_exception: Exception) -> str:
    """Gets corrected sqlite query to execute"""
    new_prompt = get_prompt_to_correct_error(previous_prompt, base_sqlite_query, sql_query_exception)
    gemini_response = await make_http_request_to_gemini(new_prompt)
    return get_cleaned_query(gemini_response)
