from telegram.ext import ApplicationBuilder, CommandHandler
from commands.start import start
from commands.debts import debts
import os


def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("debts", debts))
    app.run_polling()


if __name__ == "__main__":
    main()
