from googleapiclient.discovery import build
from datetime import datetime


def get_last_modified(creds, spreadsheet_id):
    drive_service = build("drive", "v3", credentials=creds)
    metadata = (
        drive_service.files()
        .get(fileId=spreadsheet_id, fields="modifiedTime")
        .execute()
    )
    last_modified = metadata["modifiedTime"]
    dt = datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%d.%m.%Y %H:%M")
