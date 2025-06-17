import os
from telegram import Bot, Update

ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

async def notify_admin(bot: Bot, update: Update, message: str = ""):
    if not ADMIN_USER_ID:
        return  # Переменная не задана — ничего не делаем

    user = update.effective_user
    username = user.username or "Без username"
    full_name = user.full_name or "Без имени"
    user_id = user.id

    text = (
        f"🔔 Новый контакт с ботом:\n\n"
        f"*Имя:* {full_name}\n"
        f"*Username:* @{username}\n"
        f"*ID:* `{user_id}`\n\n"
        f"{message}"
    )

    try:
        await bot.send_message(chat_id=int(ADMIN_USER_ID), text=text, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка отправки уведомления администратору: {e}")
