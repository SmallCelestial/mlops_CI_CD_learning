import pytest

import onnxruntime as ort
from tokenizers import Tokenizer

from src.sentiment_predictor import SentimentPredictor
from src.scripts.settings import Settings

settings = Settings()


@pytest.fixture
def model():
    tokenizer = Tokenizer.from_file(settings.onnx_tokenizer_path)
    ort_session = ort.InferenceSession(settings.onnx_embedding_model_path)
    ort_classifier = ort.InferenceSession(settings.onnx_classifier_path)
    return SentimentPredictor(tokenizer, ort_session, ort_classifier)


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
