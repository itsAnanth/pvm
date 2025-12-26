import requests

URL = "https://www.python.org/api/v2/downloads/release/"

def get_python_versions():
    response = requests.get(URL, timeout=10)
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

if __name__ == "__main__":
    print(get_python_versions())