import pytest
from unittest.mock import AsyncMock, MagicMock
# Adjust the import below to point to the module where return_results_html is defined.
from service.flight_query_results_renderer import return_results_html

@pytest.mark.asyncio
async def test_return_results_html(mocker):
    # Patch set_session_data in the module where it is used.
    # Replace 'service.flight_query_results_renderer' with your actual module path if different.
    mock_set_session_data = AsyncMock()
    mocker.patch(
        'service.flight_query_results_renderer.set_session_data',
        mock_set_session_data
    )

    # Patch HTMLResponse so we can intercept its creation.
    mock_html_response = MagicMock()
    mocker.patch(
        'service.flight_query_results_renderer.HTMLResponse',
        mock_html_response
    )

    # Sample input data
    base_query = "SELECT * FROM results"
    columns = ["Column1", "Column2"]
    load_more_html = "<button>Load More</button>"
    new_current_page = 0  # When zero, the rating form is included.
    rows = [["Data1", "Data2"], ["Data3", "Data4"]]
    session_id = "test_session_id"
    user_query = "Sample user query"

    # Call the function under test.
    response = await return_results_html(
        base_query,
        columns,
        load_more_html,
        new_current_page,
        rows,
        session_id,
        user_query
    )

    # Verify that set_session_data was called with the correct parameters.
    mock_set_session_data.assert_awaited_once_with(
        session_id=session_id,
        user_query=user_query,
        generated_sql=base_query,
        current_page=new_current_page
    )

    # Verify that HTMLResponse was created with content that includes key HTML components.
    # Since the content is built dynamically, we check for expected substrings.
    # For instance, verify table HTML with a column header, the load-more button, and rating form.
    called_args = mock_html_response.call_args[1]  # kwargs passed to HTMLResponse
    content = called_args.get('content', '')
    assert "<table" in content
    assert "<th class='border p-2'>Column1</th>" in content
    assert "Load More" in content
    # Since new_current_page == 0, a rating form should be present.
    assert "Rate this response" in content

    # Verify that the cookie is set correctly on the response.
    # mock_html_response.return_value simulates the HTMLResponse instance.
    mock_response_instance = mock_html_response.return_value
    mock_response_instance.set_cookie.assert_called_once_with(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600
    )

    # Verify the function returns the mocked HTMLResponse instance.
    assert response == mock_response_instance
