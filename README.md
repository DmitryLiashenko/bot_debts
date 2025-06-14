# 🏦 Debt Tracker Telegram Bot

A Telegram bot to track group debts and cash balance from Google Sheets.

---

## 🚀 Features

- ✅ Authorization by Telegram username  
- 📊 Retrieve debts from a Google Sheet  
- 🕒 Show last update time of the sheet  
- ⚙️ Easy to deploy to Fly.io  

---

## 📁 Project Structure

bot_debts/
├── main.py # Entry point of the bot
├── commands/ # Telegram bot commands
│ ├── start.py # /start command (authorization)
│ └── debts.py # /debts command (show debts)
├── services/ # Logic modules
│ ├── auth.py # User authorization
│ └── google_sheets.py # Google Sheets and Drive integration
├── requirements.txt # Python dependencies
├── README.md
├── .env # Environment variables
└── fly.toml # Fly.io configuration


## ⚙️ Setup and Deployment

1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/your-repo.git
cd bot_debts

2️⃣ Create .env file with the following content:

BOT_TOKEN=your_telegram_bot_token
SPREADSHEET_ID=your_spreadsheet_id
SOURCE_SPREADSHEET_ID=your_source_spreadsheet_id
CREDENTIALS_STR={"type":"service_account",...}  # JSON key from Google Cloud
ALLOWED_USERNAMES=user1,user2,user3

4️⃣ Run locally

python main.py
5️⃣ Deploy to Fly.io

fly launch
fly deploy

💬 Available Commands

Command	Description
/start	Authorize user by username
/debts	Show debts, cash balance and status
🗝 Environment Variables

Variable	Description
BOT_TOKEN	Telegram Bot Token
SPREADSHEET_ID	ID of the working spreadsheet
SOURCE_SPREADSHEET_ID	ID of the spreadsheet for modification dates
CREDENTIALS_STR	JSON string for Google Service Account
ALLOWED_USERNAMES	Comma-separated list of allowed usernames


BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
SPREADSHEET_ID=1A2B3C4D5E6F7G8H9I0J
SOURCE_SPREADSHEET_ID=9I8H7G6F5E4D3C2B1A
CREDENTIALS_STR={"type":"service_account",...}
ALLOWED_USERNAMES=username1,username2


📦 Install on a fresh machine (all in one):

git clone https://github.com/your-username/your-repo.git
cd bot_debts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Fill your data
python main.py

📜 License

MIT — use it freely, contribute if you want 👷