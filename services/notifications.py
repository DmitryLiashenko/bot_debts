import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

# Чтение списка разрешенных пользователей (username и номера телефонов без +)
allowed_users_raw = os.getenv("ALLOWED_USERNAMES", "")
ALLOWED_USERNAMES = [
    user.strip() for user in allowed_users_raw.split(",") if user.strip()
]

# Хранилище авторизованных пользователей на время жизни бота
AUTHORIZED_USERS = set()


def get_user_identifier(update: Update) -> str | None:
    """Возвращает username, если есть, иначе телефон (если был предоставлен)."""
    user = update.effective_user
    if user.username:
        return user.username
    contact = update.message.contact if update.message else None
    if contact and contact.phone_number:
        return contact.phone_number.replace("+", "")
    return None


def is_user_allowed(identifier: str) -> bool:
    return identifier in ALLOWED_USERNAMES


def authorize_user(identifier: str) -> bool:
    if is_user_allowed(identifier):
        AUTHORIZED_USERS.add(identifier)
        return True
    return False


def is_user_authorized(identifier: str) -> bool:
    return identifier in AUTHORIZED_USERS


# === /start команда ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if user.username:
        identifier = user.username
        if authorize_user(identifier):
            await update.message.reply_text(
                f"Привет, @{identifier}! Вы успешно авторизованы."
            )
            await notify_admin(
                context.bot,
                update,
                f"✅ @{identifier} авторизован по username.",
            )
        else:
            await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
            await notify_admin(
                context.bot,
                update,
                f"⛔️ Попытка входа от @{identifier}, но нет доступа.",
            )
    else:
        # Нет username — запрашиваем номер телефона
        button = KeyboardButton("📱 Поделиться номером", request_contact=True)
        keyboard = [[button]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )
        await update.message.reply_text(
            "Пожалуйста, поделитесь своим номером телефона для авторизации:",
            reply_markup=reply_markup,
        )
        await notify_admin(
            context.bot,
            update,
            f"📱 Пользователь без username запрашивает авторизацию по номеру телефона.",
        )


# === Обработка контакта (номер телефона) ===
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact = update.message.contact

    # 🔐 Защита: пользователь должен отправить СВОЙ номер
    if contact.user_id != update.effective_user.id:
        await update.message.reply_text(
            "❗️Пожалуйста, поделитесь именно СВОИМ номером телефона."
        )
        await notify_admin(
            context.bot,
            update,
            f"⚠️ Пользователь попытался отправить ЧУЖОЙ номер телефона: {contact.phone_number}",
        )
        return

    if contact and contact.phone_number:
        phone = contact.phone_number.replace("+", "")
        if authorize_user(phone):
            await update.message.reply_text(
                "✅ Вы успешно авторизованы по номеру телефона."
            )
            await notify_admin(
                context.bot,
                update,
                f"✅ Пользователь авторизован по номеру: {phone}",
            )
        else:
            await update.message.reply_text(
                "⛔️ Ваш номер не найден в списке авторизованных."
            )
            await notify_admin(
                context.bot,
                update,
                f"⛔️ Попытка входа по номеру {phone}, но он не разрешён.",
            )
    else:
        await update.message.reply_text("❗️ Не удалось получить номер телефона.")
        await notify_admin(
            context.bot,
            update,
            "❗️ Контакт получен, но номер не распознан.",
        )
