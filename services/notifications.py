import os
from telegram import Bot, Update
from telegram.ext import ContextTypes


def extract_identifier(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = update.effective_user

    # 1. Если есть username
    if user.username:
        return f"@{user.username}"

    # 2. Если авторизовались ранее через номер — используем сохранённый идентификатор
    identifier = context.user_data.get("identifier")
    if identifier:
        return f"📞 {identifier}"

    # 3. Ничего нет — возвращаем ID
    return f"ID: {user.id}"


async def notify_admin(
    bot: Bot, update: Update, message: str, context: ContextTypes.DEFAULT_TYPE
):
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    if not admin_chat_id:
        print("ADMIN_CHAT_ID не задан в переменных окружения")
        return

    user_info = extract_identifier(update, context)
    full_message = f"{message}\n👤 {user_info}"

    await bot.send_message(chat_id=int(admin_chat_id), text=full_message)
