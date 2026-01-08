import requests

PYTHON_ORG_URL = "https://www.python.org/api/v2/downloads/release/"
GITHUB_URL = "https://raw.githubusercontent.com/actions/python-versions/refs/heads/main/versions-manifest.json"

def get_python_org_versions():
    response = requests.get(PYTHON_ORG_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    versions = [
        release for release in data if not release['pre_release'] and "Python install manager" not in release['name'] and release['version'] >= 3
    ]

    sorted_versions = sorted(
        versions,
        key=lambda v: tuple(map(int, v['name'].replace("Python ", "").split(".")))
    )

    return sorted_versions

def get_python_github_versions():
    response = requests.get(GITHUB_URL, timeout=10)
    response.raise_for_status()
    data = response.json()


    versions = []

    for item in data:
        if bool(item["stable"]) != True or int(item["version"].split(".")[0]) < 3:
            continue


        files = item.get("files", [])
        download_url = None
        
        for file in files:
            if file['arch'] == "x64" and file['platform'] == "win32":
                download_url = file["download_url"]
                break

        if not download_url:
            continue

        versions.append({
            "version": item["version"],
            "release_url": item["release_url"],
            "download_url": download_url,
        })


    sorted_versions = sorted(
        versions,
        key=lambda v: tuple(map(int, v['version'].split(".")))
    )

    return sorted_versions

if __name__ == "__main__":
    print(get_python_github_versions())