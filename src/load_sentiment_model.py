from pathlib import Path
import zipfile

import gdown
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression


def download_file() -> None:
    url = "https://drive.google.com/uc?id=1_mUpuyHuF6gASW8v72N2vgUDh16D7xsO"
    output_dir = Path("../downloads")
    output = output_dir / "sentiment_model.zip"
    output_dir.mkdir(exist_ok=True)
    gdown.download(url, str(output), quiet=False)


def extract_zip(file_path: Path, extract_to: Path) -> None:
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def load_model_by_sentence_transformer(path: str) -> SentenceTransformer:
    return SentenceTransformer(path)


def load_model_by_joblib(path: str) -> LogisticRegression:
    return joblib.load(path)


if __name__ == "__main__":
    download_file()
    file_path = Path("../downloads/sentiment_model.zip")
    model_dir = Path("../models")
    model_dir.mkdir(exist_ok=True)

    extract_zip(file_path, extract_to=model_dir)
