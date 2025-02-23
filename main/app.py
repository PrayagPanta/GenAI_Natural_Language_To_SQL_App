import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse

from service.flight_query_results_renderer import get_results_clear_div, return_results_html
from service.flight_query_service import add_pagination_to_query, execute_sql_query
from user_session_intializer import (
    get_session_data,
    update_user_rating,
    init_db,
)
from utils import get_more_results_html_contents, get_base_sqlite_query, get_query_params_if_session


# Run database initialization only once on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Initialize the database once
    yield

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


@app.post("/query", response_class=HTMLResponse)
async def query_flights(request: Request):
    """
    Main endpoint for handling flight queries.
    It either starts a new session (and generates a new SQL query) or uses existing session data.
    The endpoint returns the full table (with cumulative rows) and the load-more button.
    The rating form is included only when there are no more results to load.
    """
    form = await request.form()
    form_query = form.get("query", "").strip()
    page_size = 100
    session_id = request.cookies.get("session_id")
    session = await get_session_data(session_id) if session_id else None

    # Determine if this is a new query or a pagination (load-more) request.
    if form_query:
        new_query, page, session_id, user_query = get_query_params_if_session(form_query, session, session_id)
    else:
        if session and session["current_page"] != 0:
            user_query = session["user_query"]
            page = session["current_page"]
            new_query = False
        else:
            return HTMLResponse(content="<p class='text-red-500'>Please enter a valid query.</p>")

    try:
        base_sqlite_query = await get_base_sqlite_query(new_query, session, user_query)

        # Ensure the query is read-only.
        if not base_sqlite_query.strip().lower().startswith("select"):
            return HTMLResponse(content=f"<p class='text-red-500'>Request Denied: {base_sqlite_query.replace('DENY:','')}.</p>")

        # Apply cumulative pagination.
        paginated_query = add_pagination_to_query(base_sqlite_query, page, page_size)
        print(f"Final Query: {paginated_query}")
        rows, columns = await execute_sql_query(paginated_query)

        # Determine if we've reached the end.
        load_more_html, new_current_page = get_more_results_html_contents(page, page_size, rows)

    except Exception as e:
        error_msg = f"Error: {str(e)}" if not str(e).startswith("DENY") else str(e)
        return HTMLResponse(content=f"<p class='text-red-500'>{error_msg}</p>")

    response = await return_results_html(base_sqlite_query, columns, load_more_html, new_current_page, rows, session_id, user_query)
    return response


@app.post("/rate")
async def rate_response(request: Request):
    """
       Endpoint to receive user rating feedback.
    """
    form = await request.form()
    rating = form.get("rating")
    session_id = request.cookies.get("session_id")
    if session_id and rating:
        try:
            await update_user_rating(session_id, rating)
        except Exception as e:
            print(f"Exception encountered during saving user rating :{e}")
    #Return an empty results container to clear the results area.
    empty_container = get_results_clear_div()
    return HTMLResponse(content=empty_container)


@app.get("/", response_class=HTMLResponse)
async def get_index_page():
    """
    Serves the main index page.
    """
    file_path = os.path.join("..", "static", "index.html")
    return FileResponse(file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, port=5001)
