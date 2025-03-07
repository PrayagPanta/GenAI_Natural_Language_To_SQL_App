from starlette.responses import HTMLResponse

from user_session_intializer import set_session_data


def get_results_clear_div_html() -> str:
    """Get div to clear results tab."""
    return """
    <div id="results-container" class="mt-4 p-6 rounded-lg shadow-lg bg-white bg-opacity-90"></div>
    """


def get_results_div_container_html(pagination_content_html: str, rating_form: str, table_content_html: str) -> str:
    """Gets results div container."""
    response_content = f"""
        <div id="result">
            {table_content_html}
        </div>
        {pagination_content_html}
        {rating_form}
    """
    return response_content


def get_rating_form_html(options_html: str) -> str:
    """Gets rating form."""
    rating_form = f"""
        <form id="rating-form" hx-post="/rate" hx-target="#results-container" hx-swap="outerHTML" class="mt-4">
            <label for="rating" class="block text-gray-700 font-medium mb-2">
                Rate this response (1-10):
            </label>
            <select id="rating" name="rating" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Select rating</option>
                {options_html}
            </select>
            <button type="submit" class="mt-2 w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition-colors">
                Submit Rating
            </button>
        </form>
        <div id="rating-message"></div>
        """
    return rating_form


def get_div_with_table_html(columns: list, rows: list) -> str:
    """Gets div with table."""
    rows_html = "".join(
        "<tr>" + "".join(f"<td class='border p-2'>{val}</td>" for val in row) + "</tr>"
        for row in rows
    )
    table_content = f"""
    <div class='overflow-auto max-h-96'>
        <table class='w-full border-collapse border border-gray-300 mt-4'>
            <thead>
                <tr class='bg-blue-100'>
                    {"".join(f"<th class='border p-2'>{col}</th>" for col in columns)}
                </tr>
            </thead>
            <tbody id="results-body">
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    return table_content


def get_pagination_content_for_control_html(load_more_html: str) -> str:
    """Gets html pagination content for control."""
    pagination_content = f"""
    <div id="pagination" class="mt-4 text-center">
        {load_more_html}
    </div>
    """
    return pagination_content


def get_no_more_results_paragraph_html() -> str:
    """Gets paragraph to display no more results when results end or are missing."""
    return "<p class='text-gray-500'>No more results.</p>"


def get_load_more_button_html(page: int) -> str:
    """Gets and Displays button to load more paginated results from the next page."""
    load_more_html = f"""
            <button hx-post="/query" hx-target="#results-container" hx-swap="innerHTML"
                    class="bg-blue-500 text-white px-4 py-2 hover:bg-blue-600">
                Load More (Page {page + 1})
            </button>
            """
    return load_more_html


async def return_results_html(base_query: str, columns: list, load_more_html: str, new_current_page: int, rows: list,
                              session_id: str, user_query: str) -> HTMLResponse:
    """Gets html table contents for the results fetched from the generated query."""
    # Build the HTML for the full table.
    table_content_html = get_div_with_table_html(columns, rows)
    # Build the pagination controls.
    pagination_content_html = get_pagination_content_for_control_html(load_more_html)
    # Only include the rating form when there are no more results to load.
    rating_form_html = ""
    if new_current_page == 0:
        options_html = "".join([f"<option value='{i}'>{i}</option>" for i in range(1, 11)])
        rating_form_html = get_rating_form_html(options_html)
    # Return only the inner content to update the existing result container.
    response_content_html = get_results_div_container_html(pagination_content_html, rating_form_html,
                                                           table_content_html)
    # Update the session data.
    await set_session_data(
        session_id=session_id,
        user_query=user_query,
        generated_sql=base_query,
        current_page=new_current_page
    )
    response = HTMLResponse(content=response_content_html)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600  # Cookie expires after 1 hour.
    )
    # if datetime.now().minute % 15 == 0:
    #     await cleanup_old_sessions()
    return response
