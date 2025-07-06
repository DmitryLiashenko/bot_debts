import os
from telegram import Bot, Update


async def notify_admin(bot: Bot, update: Update, message: str):
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    if not admin_chat_id:
        print("ADMIN_CHAT_ID не задан в переменных окружения")
        return
    # Отправляем сообщение админу
    await bot.send_message(chat_id=int(admin_chat_id), text=message)
