from telegram import Update
from telegram.ext import ContextTypes
from services.auth import authorize_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if authorize_user(user.username):
        await update.message.reply_text(
            f"Привет, @{user.username}! Вы успешно авторизованы."
        )
    else:
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
