import zipfile
from pathlib import Path
import boto3

def download_s3_file() -> None:
    bucket_name = "mlops-the-best-course"
    s3_key = "model.zip"
    local_path = Path("../downloads") / "sentiment_model.zip"

    s3 = boto3.client('s3')
    local_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket_name, s3_key, str(local_path))


def extract_zip(file_path: Path) -> None:
    extract_to = Path("../models")
    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


if __name__ == "__main__":
    local_zip_path = Path("../downloads/sentiment_model.zip")
    download_s3_file()
    extract_zip(local_zip_path)