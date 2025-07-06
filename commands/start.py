from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.auth import authorize_user
from services.notifications import notify_admin


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Если у пользователя есть username
    if user.username:
        if authorize_user(user.username):
            # Сохраняем идентификатор
            context.user_data["identifier"] = user.username
            await update.message.reply_text(
                f"Привет, @{user.username}! Вы успешно авторизованы."
            )
        else:
            await update.message.reply_text(
                "Извините, у вас нет доступа к этому боту.\n"
                "Если вы считаете, что это ошибка — свяжитесь с администратором."
            )
    else:
        # Нет username — предлагаем поделиться номером
        keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("📱 Поделиться номером", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await update.message.reply_text(
            "У вас не установлен username в Telegram.\n"
            "Пожалуйста, нажмите кнопку ниже, чтобы поделиться номером телефона для авторизации:",
            reply_markup=keyboard,
        )
