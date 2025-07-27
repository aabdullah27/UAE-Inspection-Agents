# main_agent/tools/date_tool.py
from datetime import datetime
from typing import Dict

def get_current_date() -> Dict[str, str]:
    """
    Returns the current date in a formatted string.

    This tool provides the current date, which can be used to timestamp
    reports or other documents.

    Returns:
        A dictionary containing the current date.
        e.g., {"current_date": "2025-07-28"}
    """
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return {"current_date": current_date}
    except Exception as e:
        return {"error": f"An unexpected error occurred while fetching the date: {str(e)}"}