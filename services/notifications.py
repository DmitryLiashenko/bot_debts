import os
from telegram import Bot, Update


def get_user_identifier(update: Update) -> str:
    user = update.effective_user
    if user.username:
        return f"@{user.username}"
    if (
        update.message
        and update.message.contact
        and update.message.contact.phone_number
    ):
        phone = update.message.contact.phone_number.replace("+", "")
        return f"📞 {phone}"
    return f"ID: {user.id}"  # fallback на user.id


async def notify_admin(bot: Bot, update: Update, message: str):
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    if not admin_chat_id:
        print("ADMIN_CHAT_ID не задан в переменных окружения")
        return

    user_info = get_user_identifier(update)
    full_message = f"{message}\n👤 {user_info}"

    await bot.send_message(chat_id=int(admin_chat_id), text=full_message)
