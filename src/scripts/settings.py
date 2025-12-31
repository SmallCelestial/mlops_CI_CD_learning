from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    APP_NAME: str = "my_app"

    s3_bucket_name: str = "mlops-lab11-models-sentiment"
    s3_model_key: str = "model.zip"
    onnx_embedding_model_path: str = "models/embedding_model.onnx"
    onnx_classifier_path: str = "models/classifier.onnx"
    onnx_tokenizer_path: str = "models/tokenizer/tokenizer.json"
    local_artifacts_path: str = "artifacts"

    sentence_transformer_dir: str = "models/sentence_transformer.model"
    classifier_joblib_path: str = "models/classifier.joblib"
    embedding_dim: int = 384

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        if value not in ("dev", "test", "prod"):
            raise ValueError("ENVIRONMENT must be one of: dev, test, prod")
        return value
