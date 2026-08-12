from Core.fileLister import get_file_shared_with_me
from Core.download import download_all_send_to_remote
from Core.download_zip import download_folders_as_zip_send_remote
from Core.date_check import verify_date
from Core import *
from datetime import datetime


DOWNLOAD_FOLDER = "local"


def main():

    # date = input("Enter any date less than 30 days from today :")
    date = datetime.strptime(input("Enter any date less than 30 days from today :"), "%d-%m-%Y").date()

    d,y = verify_date(date)
    if y==False:
        print(f"Not a valid date. Its {d} days behind...")
        return

    files = get_file_shared_with_me(date)

    print(f"\nFiles shared with you on {date}:\n")

    for i,file in enumerate(files,1):
        print(f"{i} : {file['name']}")

        if "size" in file:
            print(f"   Size: {file['size']} bytes")

        print(f"   ID: {file['id']}")
        print(f"   Shared: {file['sharedWithMeTime']}")
        print(f"   MimeType: {file['mimeType']}")
        print()

    print("Enter the indices of the files and folders to download:\n")

    selected_docs_idx = list(map(int, input().split()))

    confirmation = input("Download all selecte files/folders? (y/n) : ")

    if confirmation=='y':
        # download_all_send_to_remote(selected_docs,files,DOWNLOAD_FOLDER)
        download_folders_as_zip_send_remote(selected_docs_idx,files,DOWNLOAD_FOLDER)
    else:
        return

    # download_folder(
    #     service,
    #     "1xNsrmIBu1YlZUoGBu56zw7nWB_lsJ89C",
    #     "Bacterial blight disease on fruits",
    #     "./downloads"
    # )

if __name__=="__main__":
    main()