import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv("USER_NAME")
remote_server_ip = os.getenv("REMOTE_SERVER_IP")
ssh_name = user_name+'@'+remote_server_ip

remote_server_password = os.getenv("REMOTE_SERVER_PASSWORD")

# now = str(datetime.now().replace(microsecond=0))
now = str(datetime.now()).split()[0]
remote_end_folder_name = now.replace(":", "-")

base_remote_folder = "/raid/snehshah/New_Data_2/"

remote_path = f"{base_remote_folder}{remote_end_folder_name}"


def send_to_server(local_folder):

    local_folder = Path(local_folder)

    # Create the destination folder on the remote server
    try:
        subprocess.run([
            "sshpass", "-p", remote_server_password, "ssh", ssh_name, "mkdir", "-p", remote_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Could not create remote folder: {remote_path}")
        print(f"Command failed with exit code: {e.returncode}")
        return False


    for item in local_folder.iterdir():

        try:
            subprocess.run([
                "sshpass", "-p", remote_server_password, "scp", "-r", str(item), f"{ssh_name}:{remote_path}"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to transfer: {item.name}")
            print(f"Command failed with exit code: {e.returncode}")

            # Don't continue pretending everything succeeded
            return False

    return True


def clean_up():
    try:
        subprocess.run([
            "sshpass", "-p", remote_server_password, "ssh", ssh_name, f"rm -rf {remote_path}/*.zip"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code: {e.returncode}")

        # Don't continue pretending everything succeeded
        return False


def extract_zip_files():
    try:
        subprocess.run([
            "sshpass", "-p", remote_server_password, "ssh", ssh_name, f"for file in {remote_path}/*.zip; do unzip -o \"$file\" -d {remote_path}; done"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code: {e.returncode}")

        # Don't continue pretending everything succeeded
        return False

    
if __name__=="__main__":
    send_to_server("local")