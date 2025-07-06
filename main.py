import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from commands.start import start
from commands.debts import debts
from services.notifications import notify_admin
from services.auth import contact_handler


# Обёртка с уведомлением для команды /start
async def notify_start(update, context):
    await notify_admin(context.bot, update, "👋 Использует команду /start")
    await start(update, context)


# Обёртка с уведомлением для команды /debts
async def notify_debts(update, context):
    await notify_admin(context.bot, update, "💼 Использует команду /debts")
    await debts(update, context)


def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", notify_start))
    app.add_handler(CommandHandler("debts", notify_debts))

    # Обработчик отправки номера телефона (контакта)
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
