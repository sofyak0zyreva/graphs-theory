import os
import tarfile
import requests  # type: ignore
from pathlib import Path
from scripts.datasets import collect_all_datasets

# config

BASE_URL = "https://suitesparse-collection-website.herokuapp.com/MM"
DATA_DIR = Path("data")


# download


def download_file(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


# extract


def extract_tar(archive_path, extract_to):
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=extract_to)


# find mtx


def find_mtx_file(folder):
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".mtx"):
                return Path(root) / f
    return None


# main pipeline


def process_dataset(group, name):
    print(f"\n=== {name} ===")

    dataset_dir = DATA_DIR / name
    archive_path = DATA_DIR / f"{name}.tar.gz"

    # skip if already downloaded
    if dataset_dir.exists():
        print("Already exists, skipping")
        return

    url = f"{BASE_URL}/{group}/{name}.tar.gz"

    print("Downloading...")
    download_file(url, archive_path)

    print("Extracting...")
    extract_tar(archive_path, DATA_DIR)

    # find .mtx
    mtx_path = find_mtx_file(dataset_dir)

    if mtx_path is None:
        print("No .mtx found!")
    else:
        print(f"MTX found: {mtx_path}")

    # optionally remove archive
    archive_path.unlink(missing_ok=True)


def main():
    DATA_DIR.mkdir(exist_ok=True)

    for group, name in collect_all_datasets():
        try:
            process_dataset(group, name)
        except Exception as e:
            print(f"Error processing {name}: {e}")


if __name__ == "__main__":
    main()
