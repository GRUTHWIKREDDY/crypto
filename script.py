import time
import requests
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import pytz  # Import pytz for time zone handling

# Setup service account and API details
SERVICE_ACCOUNT_FILE = 'intricate-yew-424405-t2-2edb8c72faa9.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '19F7Ps74Lm532wvPjPhggbCRLvl100LVMgeQEKeh2vjs'
RANGE = 'Sheet1!A1:H100'  # Update to account for additional columns

# CoinMarketCap API Details
API_KEY = "7f372ca2-c737-40e8-a7f0-2d721abee0ea"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
PARAMS = {
    "start": "1",
    "limit": "50",
    "convert": "USD",
}
HEADERS = {
    "X-CMC_PRO_API_KEY": API_KEY,
    "Accept": "application/json",
}

# Initialize Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Setup Indian Standard Time (IST)
india_tz = pytz.timezone('Asia/Kolkata')

def fetch_crypto_data():
    """Fetch data from CoinMarketCap API."""
    response = requests.get(URL, headers=HEADERS, params=PARAMS)
    if response.status_code == 200:
        data = response.json()["data"]
        return data
    else:
        print("Error fetching data from API:", response.status_code, response.text)
        return None

def process_data(data):
    """Process the cryptocurrency data."""
    rows = [["Rank", "Name", "Symbol", "Price (USD)", "Market Cap (USD)", "24h % Change", "Last Update", "Next Update"]]

    total_price = 0
    top_5 = sorted(data, key=lambda x: x["quote"]["USD"]["market_cap"], reverse=True)[:5]
    highest_change = max(data, key=lambda x: x["quote"]["USD"]["percent_change_24h"])
    lowest_change = min(data, key=lambda x: x["quote"]["USD"]["percent_change_24h"])

    for i, crypto in enumerate(data):
        name = crypto["name"]
        symbol = crypto["symbol"]
        price = crypto["quote"]["USD"]["price"]
        market_cap = crypto["quote"]["USD"]["market_cap"]
        percent_change_24h = crypto["quote"]["USD"]["percent_change_24h"]

        # Ensure each row has 8 columns before assignment
        row = [i + 1, name, symbol, f"${price:.2f}", f"${market_cap:.2f}", f"{percent_change_24h:.2f}%", "", ""]
        rows.append(row)
        total_price += price

    average_price = total_price / len(data)

    # Add the summary at the end, ensuring each summary row has 8 columns
    rows.append([])  # Empty row for spacing
    rows.append(["Summary", "", "", "", "", "", "", ""])
    rows.append(["Top 5 Cryptocurrencies by Market Cap", "", "", "", "", "", "", ""])
    for crypto in top_5:
        rows.append([crypto["name"], f"Market Cap: ${crypto['quote']['USD']['market_cap']:.2f}", "", "", "", "", "", ""])

    rows.append([])
    rows.append([f"Highest 24h Change: {highest_change['name']} ({highest_change['quote']['USD']['percent_change_24h']:.2f}%)", "", "", "", "", "", "", ""])
    rows.append([f"Lowest 24h Change: {lowest_change['name']} ({lowest_change['quote']['USD']['percent_change_24h']:.2f}%)", "", "", "", "", "", "", ""])
    rows.append([f"Average Price of Top 50: ${average_price:.2f}", "", "", "", "", "", "", ""])

    # Get current time in IST
    last_update = datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')
    next_update = (datetime.now(india_tz) + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')

    # Ensure every row has 8 elements (columns), if not, extend it with empty strings
    for row in rows:
        while len(row) < 8:
            row.append("")  # Add empty strings for missing columns

    # Add the last and next update times in the sheet
    for row in rows[1:]:  # Exclude the header row
        row[6] = last_update  # Last Update column
        row[7] = next_update  # Next Update column

    return rows

def update_sheet(rows):
    """Update Google Sheet with processed data."""
    body = {"values": rows}
    try:
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE,
            valueInputOption="RAW",
            body=body,
        ).execute()
        print("Crypto data updated successfully.")
    except Exception as e:
        print("Error updating sheet:", e)

def main():
    """Main function to fetch, process, and update crypto data every 5 minutes."""
    while True:
        print("Fetching crypto data...")
        crypto_data = fetch_crypto_data()
        if crypto_data:
            rows = process_data(crypto_data)
            update_sheet(rows)
        else:
            print("Failed to fetch data.")

        print("Waiting for 5 minutes...")
        time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    main()
