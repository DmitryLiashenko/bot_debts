from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.auth import authorize_user, is_user_authorized
from services.notifications import notify_admin


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Если есть username и он разрешён
    if user.username and authorize_user(user.username):
        context.user_data["identifier"] = user.username
        await update.message.reply_text(
            f"Привет, @{user.username}! Вы успешно авторизованы."
        )
        return

    # Если уже есть сохранённый identifier в user_data (например, номер телефона)
    identifier = context.user_data.get("identifier")
    if identifier and is_user_authorized(identifier):
        await update.message.reply_text(
            f"Привет, {identifier}! Вы уже авторизованы ранее."
        )
        return

    # Нет username и не авторизован — запрашиваем номер
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Поделиться номером", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await update.message.reply_text(
        "У вас не установлен username в Telegram или вы ещё не авторизованы.\n"
        "Пожалуйста, нажмите кнопку ниже, чтобы поделиться номером телефона для авторизации:",
        reply_markup=keyboard,
    )
