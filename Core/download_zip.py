from playwright.sync_api import sync_playwright
from pathlib import Path
from Core.send_remote import send_to_server,extract_zip_files
import shutil


def delete_download_folder_contents(download_folder):
    download_folder = Path(download_folder)

    for item in download_folder.iterdir():

        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def download_folder_as_zip_send_remote(folder_id, folder_name, download_folder):

    download_folder = Path(download_folder)
    download_folder.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:

        context = p.chromium.launch_persistent_context(
            "browser_profile",
            headless=False,
            accept_downloads=True
        )

        page = context.pages[0] if context.pages else context.new_page()

        drive_url = f"https://drive.google.com/drive/shared-with-me"
        print("Opening folder...")
        page.goto(drive_url)

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)

        folder = page.get_by_text(
            folder_name,
            exact=True
        )
        folder.click(button="right")

        page.wait_for_timeout(1000)

        # Wait for the download while clicking Download
        with page.expect_download(timeout=600000) as download_info:
            page.get_by_role("menuitem", name="Download").click()

        download = download_info.value
        zip_path = download_folder / download.suggested_filename
        download.save_as(zip_path)

        print(f"Downloaded: {zip_path}")
        context.close()


        success_code = send_to_server(download_folder)
        if success_code:
            print("File moved to the server\n")
            extract_zip_files()
        else:
            print("Transfer failed...")


        # Delete everything locally
        delete_download_folder_contents(download_folder)

        return zip_path


def download_folders_as_zip_send_remote(selected_docs_idx,files,dest_folder):

    for i in selected_docs_idx:
        file_name = files[i]['name']
        file_id = files[i]['id']
        download_folder_as_zip_send_remote(file_id,file_name,dest_folder)

    #Clean-up; delete the folder after all the files are downloaded & transferred.
    shutil.rmtree(dest_folder)