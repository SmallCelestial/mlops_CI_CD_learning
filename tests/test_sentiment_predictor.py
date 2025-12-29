import pytest

from src.sentiment_predictor import SentimentPredictor
from src.settings import Settings

settings = Settings()


@pytest.fixture
def model():
    return SentimentPredictor(
        settings.transformer_model_path, settings.classifier_model_path
    )


def test_predict_raise_error_if_input_text_is_empty(model):
    with pytest.raises(ValueError):
        model.predict("")

    with pytest.raises(ValueError):
        model.predict(None)

    with pytest.raises(ValueError):
        model.predict(123)


def test_predict_return_negative_if_input_text_is_negative(model):
    assert model.predict("I hate this movie") == "negative"


def test_predict_return_neutral_if_input_text_is_neutral(model):
    assert model.predict("This is movie") == "neutral"


def test_predict_return_positive_if_input_text_is_positive(model):
    assert model.predict("I love this movie") == "positive"
