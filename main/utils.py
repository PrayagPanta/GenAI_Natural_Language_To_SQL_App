import uuid

from prompts.nlp_to_sql_prompt import get_formatted_nlp_to_sql_prompt
from service.flight_query_results_renderer import get_no_more_results_paragraph, get_load_more_button
from service.flight_query_service import get_cleaned_query
from service.gemini_service import make_http_request_to_gemini


def get_more_results_html_contents(page, page_size, rows):
    if len(rows) < page * page_size:
        load_more_html = get_no_more_results_paragraph()
        new_current_page = 0  # End pagination.
    else:
        load_more_html = get_load_more_button(page)
        new_current_page = page + 1
    return load_more_html, new_current_page


async def get_base_sqlite_query(new_query, session, user_query):
    if new_query:
        prompt = get_formatted_nlp_to_sql_prompt(user_query)
        gemini_response = await make_http_request_to_gemini(prompt)
        base_query = get_cleaned_query(gemini_response)
    else:
        base_query = session["generated_sql"]
    return base_query


def get_query_params_if_session(form_query, session, session_id):
    if session and session["user_query"] == form_query and session["current_page"] != 0:
        user_query = form_query
        page = session["current_page"]
        new_query = False
    else:
        user_query = form_query
        session_id = str(uuid.uuid4())
        page = 1
        new_query = True
    return new_query, page, session_id, user_query
