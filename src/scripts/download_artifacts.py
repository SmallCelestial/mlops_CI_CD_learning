import zipfile
from pathlib import Path

import boto3

from src.scripts.settings import Settings


def download_artifacts(settings: Settings):
    local_zip_path = Path(settings.local_artifacts_path) / "model.zip"
    extract_to_path = Path("models")

    local_zip_path.parent.mkdir(parents=True, exist_ok=True)
    extract_to_path.mkdir(parents=True, exist_ok=True)

    print(
        f"Downloading s3://{settings.s3_bucket_name}/{settings.s3_model_key} to {local_zip_path}"
    )
    s3 = boto3.client("s3")
    s3.download_file(settings.s3_bucket_name, settings.s3_model_key, str(local_zip_path))
    print("Download complete.")

    # Extract the zip file
    print(f"Extracting {local_zip_path} to {extract_to_path}")
    with zipfile.ZipFile(local_zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to_path)
    print("Extraction complete.")

if __name__ == "__main__":
    settings = Settings()
    download_artifacts(settings)