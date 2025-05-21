# 🤖 Telegram Bot for Tracking Debts via Google Sheets

A simple Telegram bot that helps track group debts, balances, and cash flows, using **Google Sheets** as a backend. Only authorized Telegram users can access the data.

---

## 🚀 Features

- 🔐 **User authentication** via `/start`
- 📊 **View debts and balances** via `/debts`
- 📁 **Google Sheets integration** for real-time data

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/DmitryLiashenko/bot_debts.git
cd bot_debts
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Secrets to `.env`

Create a file named `.env` in the project root:

```dotenv
BOT_TOKEN=your_telegram_bot_token
SPREADSHEET_ID=your_google_sheet_id
credentials_str={"type": "...", "project_id": "..."}  # JSON string from Google credentials
ALLOWED_USERNAMES=user1,user2,user3
```

> ⚠️ **Keep your `.env` and any credential `.json` files out of version control.**  
> Use a `.gitignore` file to prevent them from being committed:

**.gitignore**
```
.env
*.json
```

---

### 4. Run the Bot

```bash
python bot.py
```

---

## 📦 Deployment

You can deploy the bot to platforms that support Python and environment variables.  
Examples:

### ✅ Fly.io (with Docker)

1. **Create a `Dockerfile`** in your project root (example below)
2. **Install the Fly.io CLI** and run:
   ```bash
   fly launch
   fly deploy
   ```

**Example `Dockerfile`:**
```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
```

Don't forget to set secrets:

```bash
fly secrets set BOT_TOKEN=xxx SPREADSHEET_ID=xxx credentials_str='{"type":"service_account",...}' ALLOWED_USERNAMES=user1,user2
```

> Optionally, use other platforms like Railway, Render, Heroku, etc.

---

## 🧪 Manual Testing

You can test the bot by sending these commands in Telegram:

- `/start` – authorizes the user
- `/debts` – fetches and displays debts, balances, and cash data

---

## 📁 Project Structure

```
.
├── bot.py               # Main bot logic
├── .env                 # Environment variables (NOT in git)
├── requirements.txt     # Project dependencies
├── Dockerfile           # For deployment (optional)
└── README.md            # Project documentation
```
