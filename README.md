Crypto Market Data Updater
This project fetches real-time cryptocurrency data from the CoinMarketCap API and updates it to a Google Sheet. The script runs continuously to provide live updates every 5 minutes.

Features
Fetches the top 50 cryptocurrencies with their:
Rank
Name
Symbol
Price (USD)
Market Cap (USD)
24-hour percentage change
Last update time
Next update time
Computes summary statistics:
Top 5 cryptocurrencies by market cap
Cryptocurrency with the highest 24-hour change
Cryptocurrency with the lowest 24-hour change
Average price of the top 50 cryptocurrencies
Outputs a well-structured and formatted Google Sheet.
Setup Instructions
1. Requirements
Python 3.8+
EC2 instance (AWS Linux/Ubuntu)
Google Sheets API credentials
CoinMarketCap API key
2. Project Structure
bash
Copy code
Crypto/
├── script.py                # Main script
├── requirements.txt         # Python dependencies
├── intricate-yew-424405-t2-2edb8c72faa9.json  # Google API credentials
3. Installation
Upload the Project to the EC2 Instance
Use scp to copy the project folder to your EC2 instance.

bash
Copy code
scp -i /path/to/key.pem -r /path/to/Crypto ec2-user@<your-ec2-public-ip>:~/Crypto
Connect to the EC2 Instance

bash
Copy code
ssh -i /path/to/key.pem ec2-user@<your-ec2-public-ip>
Navigate to the Project Directory

bash
Copy code
cd ~/Crypto
Install Python and Dependencies

bash
Copy code
sudo yum install python3 -y
pip3 install -r requirements.txt
4. Running the Script Continuously
Install tmux (if not already installed):

bash
Copy code
sudo yum install tmux -y
Start a tmux session:

bash
Copy code
tmux new -s crypto_script
Run the script:

bash
Copy code
python3 script.py
Detach the tmux session to keep the script running:

Press Ctrl + B, then D.
Reattach to the tmux session later:

bash
Copy code
tmux attach -t crypto_script
How to Update the Script
Open the file using a text editor (e.g., Nano):

bash
Copy code
nano script.py
Make changes and save:

Press Ctrl + O, then Enter to save.
Press Ctrl + X to exit.
Restart the script if necessary.

Environment Variables
Ensure the following values are correctly set:

SERVICE_ACCOUNT_FILE: Path to the Google API credentials JSON file.
SPREADSHEET_ID: ID of the Google Sheet to be updated.
API_KEY: CoinMarketCap API key.
Troubleshooting
Google Sheets API Errors:

Ensure the Google API credentials file is correct and accessible.
Verify that the Google Sheet ID and range are correct.
Connection Errors:

Ensure internet access is available on the EC2 instance.
Validate API keys for both Google Sheets and CoinMarketCap.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributions
Contributions are welcome! Please fork the repository and submit a pull request.
