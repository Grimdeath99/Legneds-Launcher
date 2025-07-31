import requests
import zipfile
import io
from settings import get_setting

def download_latest_dolphin(dest_folder):
    api_url = get_setting("DOLPHIN_RELEASE_API")
    headers = {"Accept": "application/vnd.github.v3+json"}
    resp = requests.get(api_url, headers=headers)
    data = resp.json()
    asset = None
    for a in data["assets"]:
        if "windows" in a["name"].lower() and a["name"].endswith(".zip"):
            asset = a
            break
    if asset:
        print("Downloading:", asset["name"])
        zip_resp = requests.get(asset["browser_download_url"])
        with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as z:
            z.extractall(dest_folder)
        print("Legends Updated!")
    else:
        print("No suitable build found.")
