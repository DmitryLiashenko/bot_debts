import os
import json
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SOURCE_SPREADSHEET_ID = os.getenv("SOURCE_SPREADSHEET_ID")
credentials_str = os.getenv("CREDENTIALS_STR")

if not all([BOT_TOKEN, SPREADSHEET_ID, SOURCE_SPREADSHEET_ID, credentials_str]):
    raise ValueError("Не заданы все обязательные переменные окружения")

credentials_dict = json.loads(credentials_str)
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]
creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


def get_debts_data():
    data = sheet.get_all_values()
    rows = data[1:17]

    dolgimy = ["*ДОЛГИ МЫ*"]
    dolginam = ["*ДОЛГИ НАМ*"]
    kassa = ["*КАССА*"]
    balans = ["*БАЛАНС*"]

    for row in rows:
        if len(row) > 2 and (row[0] or row[2]):
            dolgimy.append(f"{row[0]} — {row[2]}")
        if len(row) > 5 and (row[4] or row[5]):
            dolginam.append(f"{row[4]} — {row[5]}")
        if len(row) > 8 and (row[7] or row[8]):
            kassa.append(f"{row[7]} — {row[8]}")

    balance_value = sheet.acell("A20").value
    if balance_value:
        balans.append(balance_value)

    return [
        "\n".join(dolgimy),
        "\n".join(dolginam),
        "\n".join(kassa),
        "\n".join(balans),
    ]
