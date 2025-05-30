import os  

allowed_users_raw = os.getenv("ALLOWED_USERNAMES", "")
ALLOWED_USERNAMES = [
    user.strip() for user in allowed_users_raw.split(",") if user.strip()
]

AUTHORIZED_USERS = set()


# Check if a username is allowed (from ALLOWED_USERNAMES list)
def is_user_allowed(username: str) -> bool:
    return username in ALLOWED_USERNAMES


# Add a user to the authorized list if they are allowed
def authorize_user(username: str) -> bool:
    if is_user_allowed(username):
        AUTHORIZED_USERS.add(username)
        return True
    return False


# Check if a user has already been authorized (via /start command)
def is_user_authorized(username: str) -> bool:
    return username in AUTHORIZED_USERS
