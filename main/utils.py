from prompts.nlp_to_sql_prompt import get_formatted_nlp_to_sql_prompt
from service.flight_query_results_renderer import get_no_more_results_paragraph_html, get_load_more_button_html
from service.flight_query_service import get_cleaned_query
from service.gemini_service import make_http_request_to_gemini


def get_more_results_html_contents(page: int, page_size: int, rows: list) -> tuple:
    """Fetches more results until the end of pagination is reached."""
    if len(rows) < page_size:
        load_more_html = get_no_more_results_paragraph_html()
        new_current_page = 0  # End pagination.
    else:
        load_more_html = get_load_more_button_html(page)
        new_current_page = page + 1
    return load_more_html, new_current_page


async def get_prompt_and_base_sqlite_query(new_query: str, session: dict, user_query: str) -> tuple[str, str]:
    """Gets base sqlite query to execute"""
    if new_query:
        prompt = get_formatted_nlp_to_sql_prompt(user_query)
        gemini_response = await make_http_request_to_gemini(prompt)
        base_query = get_cleaned_query(gemini_response)
    else:
        prompt = session["user_query"]
        base_query = session["generated_sql"]
    return prompt, base_query


def get_query_params_if_session(form_query: str, session: dict) -> tuple:
    """Fetches query parameters based on user session"""
    if session and session["user_query"] == form_query and session["current_page"] != 0:
        user_query = form_query
        page = session["current_page"]
        new_query = False
    else:
        user_query = form_query
        page = 1
        new_query = True
    return new_query, page, user_query
