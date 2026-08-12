import os.path
from datetime import datetime, timedelta, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from dotenv import load_dotenv
load_dotenv()


# SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

IST = timezone(timedelta(hours=5, minutes=30))


def authenticate():
    creds = None

    # token.json contains your login session after first authentication
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("CLIENT_SECRET_FILE_NAME"),
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save credentials for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def list_files():
    creds = authenticate()

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    results = service.files().list(
        pageSize=100,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get("files", [])

    print(f"Found {len(files)} files:")
    print(files[0].get("name"))

    for file in files:
        print(
            f"{file['name']} "
            f"({file['mimeType']}) "
            f"[{file['id']}]"
        )



def get_file_shared_with_me(date):
    creds = authenticate()

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    #start and end time
    # now = datetime.now(IST)

    # start_of_day = now.replace(
    #     hour=0,
    #     minute=0,
    #     second=0,
    #     microsecond=0
    # )

    start_of_day = datetime.combine(date, datetime.min.time(),tzinfo=IST)

    start_of_tomorrow = start_of_day + timedelta(days=1)

    query = (
        "sharedWithMe = true "
        "and trashed = false"
    )

    results = service.files().list(
        q=query,
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType, size, sharedWithMeTime)"
    ).execute()

    all_files =  results.get("files", [])

    files_shared_today = []

    for file in all_files:

        shared_time_str_utc = file['sharedWithMeTime']
        if not shared_time_str_utc:
            continue

        # Convert Google's timestamp to datetime
        shared_time = datetime.fromisoformat(
            shared_time_str_utc.replace("Z", "+00:00")
        )

        shared_time_str_ist = shared_time.astimezone(IST)

        # Check whether it was shared today
        if start_of_day <= shared_time_str_ist < start_of_tomorrow:
            files_shared_today.append(file)

    return files_shared_today


if __name__ == "__main__":
    # list_files()
    files = get_file_shared_with_me()

    print("\nFiles shared with you today:\n")

    for i,file in enumerate(files,1):
        print(f"{i} : {file['name']}")

        if "size" in file:
            print(f"   Size: {file['size']} bytes")

        print(f"   ID: {file['id']}")
        print(f"   Shared: {file['sharedWithMeTime']}")
        print(f"   MimeType: {file['mimeType']}")
        print()