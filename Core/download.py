import os
import shutil

from googleapiclient.http import MediaIoBaseDownload
from Core.fileLister import authenticate
from googleapiclient.discovery import build
from pathlib import Path
from Core.send_remote import send_to_server


DOWNLOAD_FOLDER = "local"

creds = authenticate()
service = build(
    "drive",
    "v3",
    credentials=creds
)


def download_file(file_id, file_name, destination_folder):

    os.makedirs(destination_folder, exist_ok=True)
    file_path = os.path.join(destination_folder, file_name)

    request = service.files().get_media(fileId=file_id)

    with open(file_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(
                    f"\rDownloading {file_name}: "
                    f"{int(status.progress() * 100)}%",
                    end=""
                )
    print(f"\nDownloaded: {file_path}")




def list_folder(service, folder_id):

    query = (
        f"'{folder_id}' in parents "
        "and trashed = false"
    )

    results = service.files().list(
        q=query,
        pageSize=1000,
        fields="files(id, name, mimeType, size)"
    ).execute()

    return results.get("files", [])




def download_folder(folder_id, folder_name, destination):

    folder_path = os.path.join(destination, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    files = list_folder(service, folder_id)

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        mime_type = file["mimeType"]

        if mime_type == "application/vnd.google-apps.folder":

            download_folder(
                file_id,
                file_name,
                folder_path
            )
        else:
            download_file(
                file_id,
                file_name,
                folder_path
            )



def delete_download_folder_contents(download_folder):
    download_folder = Path(download_folder)

    for item in download_folder.iterdir():

        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def download_all_send_to_remote(selected_docs, files, dest):

    for i in selected_docs:
        file_id = files[i]['id']
        name = files[i]['name']

        if files[i]['mimeType'] == "application/vnd.google-apps.folder":
            download_folder(file_id, name, dest)
        else:
            download_file(file_id, name, dest)

        success_code = send_to_server(DOWNLOAD_FOLDER)
        if success_code:
            print("File moved to the server\n")
        else:
            print("Transfer failed...")

        # Delete everything locally
        delete_download_folder_contents(DOWNLOAD_FOLDER)

    shutil.rmtree(DOWNLOAD_FOLDER)

        
            