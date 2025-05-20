import os, gspread, json
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler


# Загружает переменные из .env
load_dotenv() 
credentials_str = os.getenv("credentials_str")
credentials_dict = json.loads(credentials_str)
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
allowed_users_raw = os.getenv("ALLOWED_USERNAMES", "")
ALLOWED_USERNAMES = [user.strip() for user in allowed_users_raw.split(",") if user.strip()]
# Храним авторизованных пользователей на время текущей сессии бота
AUTHORIZED_USERS = set()


# ===== Авторизация для Google Sheets =====

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


# ===== Команда /start — авторизация =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.username in ALLOWED_USERNAMES:
        AUTHORIZED_USERS.add(user.username)
        await update.message.reply_text(f"Привет, @{user.username}! Вы успешно авторизованы.")
    else:
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")


# ===== Команда /debts =====
async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username not in AUTHORIZED_USERS:
        await update.message.reply_text("Пожалуйста, авторизируйтесь сначала через команду /start.")
        return

    try:
        data = sheet.get_all_values()
        rows = data[1:17]  # строки 2-15

        dolgimy = ["*ДОЛГИ МЫ*"]
        dolginam = ["*ДОЛГИ НАМ*"]
        kassa = ["*КАССА*"]
        balans = ["*БАЛАНС*"]

        for row in rows:
            # Долги МЫ: A и C (индексы 0 и 2)
            if len(row) > 2 and (row[0] or row[2]):
                dolgimy.append(f"{row[0]} — {row[2]}")

            # Долги НАМ: E и F (индексы 4 и 5)
            if len(row) > 5 and (row[4] or row[5]):
                dolginam.append(f"{row[4]} — {row[5]}")

            # Касса: H и I (индексы 7 и 8)
            if len(row) > 8 and (row[7] or row[8]):
                kassa.append(f"{row[7]} — {row[8]}")

            # Получаем ячейку A20
        balance_value = sheet.acell('A20').value
        if balance_value:
            balans.append(balance_value)


        await update.message.reply_text("\n".join(dolgimy), parse_mode='Markdown')
        await update.message.reply_text("\n".join(dolginam), parse_mode='Markdown')
        await update.message.reply_text("\n".join(kassa), parse_mode='Markdown')
        await update.message.reply_text("\n".join(balans), parse_mode='Markdown')
        if int(balans[1]) < 0:
            await update.message.reply_text("💸 Касса в минусе — пора сдавать бутылки!\n👷‍♂️ Мужики, когда работать будете?!")
        elif int(balans[1]) > 0:
            await update.message.reply_text("О,можно и поделить денюжку)))")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
    

# ===== Run Bot =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("debts", get_data))
    app.run_polling()
    


if __name__ == "__main__":
    main()