import os

allowed_users_raw = os.getenv("ALLOWED_USERNAMES", "")
ALLOWED_USERNAMES = [
    user.strip() for user in allowed_users_raw.split(",") if user.strip()
]
AUTHORIZED_USERS = set()


def is_user_allowed(username: str) -> bool:
    return username in ALLOWED_USERNAMES


def authorize_user(username: str) -> bool:
    if is_user_allowed(username):
        AUTHORIZED_USERS.add(username)
        return True
    return False


def is_user_authorized(username: str) -> bool:
    return username in AUTHORIZED_USERS
