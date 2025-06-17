import os
from telegram.ext import ApplicationBuilder, CommandHandler
from commands.start import start
from commands.debts import debts
from services.notifications import notify_admin


async def notify_start(update, context):
    await notify_admin(context.bot, update, "👋 Использует команду /start")
    await start(update, context)


async def notify_debts(update, context):
    await notify_admin(context.bot, update, "💼 Использует команду /debts")
    await debts(update, context)


def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", notify_start))
    app.add_handler(CommandHandler("debts", notify_debts))
    app.run_polling()


if __name__ == "__main__":
    main()
