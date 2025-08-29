import requests
import zipfile
import io
import os
from settings import get_setting

def check_for_updates():
    api_url = get_setting("API_URL") + "check_updates"
    headers = {"Accept": "application/json"}
    resp = requests.get(api_url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        if data.get("update_available", False):
            return data.get("version", "Unknown")
        else:
            return None
    else:
        print("Error checking for updates:", resp.status_code, resp.text)
        return None

def download_latest_dolphin(dest_folder, progress_callback=None):
    api_url = get_setting("DOLPHIN_RELEASE_API")
    headers = {"Accept": "application/vnd.github.v3+json"}
    resp = requests.get(api_url, headers=headers)
    data = resp.json()
    asset = None
    for a in data.get("assets", []):
        if "windows" in a["name"].lower() and a["name"].endswith(".zip"):
            asset = a
            break
    if asset:
        print("Downloading:", asset["name"])
        download_url = asset["browser_download_url"]
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            chunks = []
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    chunks.append(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(min(downloaded / total, 1.0))
            zip_data = b''.join(chunks)
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            z.extractall(dest_folder)
        print("Legends Updated!")
    else:
        print("No suitable build found.")

def download_latest_alpha(dest_folder, progress_callback=None):
    # Download master branch zip from GitHub
    repo = "Smash-Bros-Legends"
    branch = "master"
    zip_url = f"https://github.com/{repo}/archive/{branch}.zip"
    with requests.get(zip_url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        downloaded = 0
        chunks = []
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                chunks.append(chunk)
                downloaded += len(chunk)
                if progress_callback and total:
                    progress_callback(min(downloaded / total, 1.0))
        zip_data = b''.join(chunks)
    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        z.extractall(dest_folder)
    print("Alpha build updated!")

def check_for_github_update(current_version):
    update_source = get_setting("UPDATE_SOURCE")
    if update_source == "github_releases":
        # Main: Check latest release
        api_url = "https://api.github.com/repos/Smash-Bros-Legends/releases/latest"
        resp = requests.get(api_url)
        if resp.status_code == 200:
            data = resp.json()
            latest_version = data.get("tag_name", "")
            if latest_version and latest_version != current_version:
                return latest_version
            else:
                return None
        else:
            print("GitHub API error:", resp.status_code)
            return None
    elif update_source == "github_master":
        # Alpha: Check latest commit on master
        api_url = "https://api.github.com/repos/Smash-Bros-Legends/commits/master"
        resp = requests.get(api_url)
        if resp.status_code == 200:
            data = resp.json()
            latest_sha = data.get("sha", "")
            # You may want to store the last known sha in your app for comparison
            return latest_sha
        else:
            print("GitHub API error:", resp.status_code)
            return None
    else:
        print("Unknown update source.")
        return None
