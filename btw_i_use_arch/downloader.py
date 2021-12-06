import requests
import shutil


def download_file(url):
    """Downloads file from parameter using requests and shutil

    Args:
        url (string): URL of file to be downloaded

    Returns:
        string: filename of the downloaded file
    """
    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


def get_latest_release_tarball(url):
    """Finds the latest release from Github and downloads it

    Args:
        url (string): an API url containing a JSON response

    Returns:
        string: a url containing the tarball
    """
    res = requests.get(url)
    assets = res.json()["assets"]
    for asset in assets:
        if asset["browser_download_url"][-6:] == "tar.gz":
            return asset["browser_download_url"]
        else:
            pass
    return "Latest tarball not found!"
