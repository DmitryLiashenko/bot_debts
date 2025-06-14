from telegram import Update
from telegram.ext import ContextTypes
from services.auth import is_user_authorized
from services.get_last_modified import get_last_modified
from services.google_sheets import (
    get_debts_data,
    creds,
    SOURCE_SPREADSHEET_ID,
)


async def debts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_user_authorized(user.username):
        await update.message.reply_text(
            "Пожалуйста, авторизируйтесь сначала через команду /start."
        )
        return

    try:
        result_messages = get_debts_data()
        for message in result_messages:
            await update.message.reply_text(message, parse_mode="Markdown")

        formatted_time = get_last_modified(creds, SOURCE_SPREADSHEET_ID)
        await update.message.reply_text(
            f"📅 Последнее обновление таблицы: {formatted_time}"
        )

        if int(result_messages[-1].splitlines()[-1]) < 0:
            await update.message.reply_text(
                "💸 Касса в минусе — пора сдавать бутылки!\n👷‍♂️ Мужики, когда работать будете?!"
            )
        else:
            await update.message.reply_text("О,можно и поделить денюжку)))")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
