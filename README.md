# Google Drive → SSH Server Automated Data Transfer

An automation tool that transfers selected files and folders from **Google Drive to a remote SSH server**.

The tool uses the **Google Drive API** to identify files and folders shared with the user within a specified date range. The user can then select which items to transfer.

For folders, the tool uses **Playwright** to automate the Google Drive web interface and download the folder as a **ZIP archive**. The ZIP is then transferred to the remote server using **SSH/SCP**, extracted remotely, and cleaned up automatically.

---

## Features

- Lists files and folders shared with the user within the specified date range.
- Supports date validation and filtering.
- Handles both files and folders.
- Uses Playwright to automate Google Drive's web UI.
- Downloads Google Drive folders as ZIP archives.
- Transfers ZIP archives to the remote server using SSH/SCP.
- Automatically extracts ZIP files on the remote server.
- Automatically cleans up temporary local and remote ZIP files.
- Uses environment variables for SSH credentials and configuration.
- Handles transfer failures without unnecessarily deleting local data.

---

## Project Structure

```text
.
├── Core
│   ├── date_check.py       # Verifies whether a date is within the allowed range
│   ├── download.py         # Downloads files using the Google Drive API
│   ├── download_zip.py     # Downloads folders as ZIP files using Playwright
│   ├── fileLister.py       # Lists files/folders shared within the date range
│   └── send_remote.py      # Transfers files/ZIPs to the remote server
│
├── main.py                 # Main driver program
├── README.md
└── requirements.txt        # Python dependencies

```

# Setup

### 1. Set up your environment
 
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
 
pip install -r requirements.txt
playwright install             # Installs the browser binaries Playwright needs
```

### 2. Get your Google Drive API credentials
 
1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Create a **new project**
3. Navigate to **APIs & Services → Library**, and enable the **Google Drive API**
4. Go to **APIs & Services → OAuth consent screen** and configure it
5. Under **Credentials**, create an **OAuth client ID**
6. Download the client credentials JSON file and place it in the **project root directory**

### 3. Configure environment variables
 
Create a `.env` file in the project root:
 
```env
USER_NAME=your_ssh_username
REMOTE_SERVER_IP=your_remote_server_ip
REMOTE_SERVER_PASSWORD=your_ssh_password
CLIENT_SECRET_FILE_NAME=client_secret.json
```
 
| Variable | Description |
|---|---|
| `USER_NAME` | SSH username for the remote server |
| `REMOTE_SERVER_IP` | IP address or hostname of the remote server |
| `REMOTE_SERVER_PASSWORD` | SSH password for authentication |
| `CLIENT_SECRET_FILE_NAME` | Filename of your downloaded Google OAuth client secret JSON |
 
---
 

## Usage
 
From the project root, simply run:
 
```bash
python main.py
```
 
You'll be prompted to select which discovered files/folders to archive and transfer. The tool handles the rest — zipping, uploading, unzipping, and cleanup — automatically.
 
---
 
## Notes
 
- Only files/folders modified within the configured window (default: 30 days) are listed for selection.
- The `local/` folder is used purely as scratch space and is deleted after each run completes.
- Remote `.zip` archives are removed after successful extraction to keep the server tidy.
---


