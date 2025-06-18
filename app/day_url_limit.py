import re
from datetime import datetime, timedelta

def filter_urls_last_7_days(urls):
    """
    Filters a list of URLs and returns only those whose path contains a date (YYYY/MM/DD)
    within the last 7 days from today.

    Args:
        urls (list): List of URLs as strings.

    Returns:
        list: URLs with dates in the last 7 days.
    """
    filtered = []
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    date_pattern = re.compile(r'/(\d{4})/(\d{2})/(\d{2})/')

    for url in urls:
        match = date_pattern.search(url)
        if match:
            year, month, day = map(int, match.groups())
            url_date = datetime(year, month, day)
            if week_ago <= url_date <= today:
                filtered.append(url)
    return filtered

# Example usage:
if __name__ == "__main__":
    test_urls = [
        "https://www.gurnee.il.us/news/2025/06/12/village-board-approves-five-year-extension-with-waste-management-for-commercial-waste-hauling-services",
        "https://www.gurnee.il.us/news/2025/02/10/ethylene-oxide-update--64--february-10--2025"
    ]
    print(filter_urls_last_7_days(test_urls))