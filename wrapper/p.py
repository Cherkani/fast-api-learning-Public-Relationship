import requests
from datetime import datetime

def get_earnings_calendar(ticker, api_key, limit=10):
    url = f"https://api.api-ninjas.com/v1/earningscalendar?ticker={ticker}"
    headers = {
        "X-Api-Key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        limited_data = data[:limit]
        
        return limited_data
    else:
        return f"Error: {response.status_code}, {response.text}"

def filter_and_format_earnings_data(earnings_data):
    filtered_data = []
    for entry in earnings_data:
        date_str = entry.get("pricedate")
        formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y/%m/%d") if date_str else "N/A"
        formatted_entry = {
            "Date": formatted_date,
            "Ticker": entry.get("ticker", "N/A"),
            "Actual EPS": f"{entry.get('actual_eps', 'N/A'):.2f}" if entry.get('actual_eps') is not None else "N/A",
            "Estimated EPS": f"{entry.get('estimated_eps', 'N/A'):.2f}" if entry.get('estimated_eps') is not None else "N/A",
            "Actual Revenue": entry.get("actual_revenue", "N/A"),
            "Estimated Revenue": entry.get("estimated_revenue", "N/A")
        }

        filtered_data.append(formatted_entry)
    return filtered_data

if __name__ == "__main__":
    api_key = "AJFDZyqIR7ZXTlxF6AdfWg==Sq78VNwxlo750ia8"
    ticker = "MSFT"
    limit = 2
    earnings_data = get_earnings_calendar(ticker, api_key, limit)
    if isinstance(earnings_data, list):
        formatted_data = filter_and_format_earnings_data(earnings_data)
        for entry in formatted_data:
            print(entry)
    else:
        print(earnings_data)
