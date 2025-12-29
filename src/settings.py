from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    APP_NAME: str = "my_app"

    transformer_model_path: str = "models/sentence_transformer.model"
    classifier_model_path: str = "models/classifier.joblib"

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        if value not in ("dev", "test", "prod"):
            raise ValueError("ENVIRONMENT must be one of: dev, test, prod")
        return value
