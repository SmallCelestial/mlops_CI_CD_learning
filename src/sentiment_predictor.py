import numpy as np
from onnxruntime import InferenceSession
from tokenizers import Tokenizer

SENTIMENT_MAP = {
    0: "negative",
    1: "neutral",
    2: "positive"
}


class SentimentPredictor:
    def __init__(self, tokenizer: Tokenizer, embedding_session: InferenceSession, ort_classifier: InferenceSession):
        self.tokenizer = tokenizer
        self.embedding_session = embedding_session
        self.classifier_session = ort_classifier

    def predict(self, text: str, as_string: bool = True) -> int | str:
        if not text or not isinstance(text, str):
            raise ValueError("Input text is empty")

        # tokenize input
        encoded = self.tokenizer.encode(text)

        # prepare numpy arrays for ONNX
        input_ids = np.array([encoded.ids])
        attention_mask = np.array([encoded.attention_mask])

        # run embedding inference
        embedding_inputs = {"input_ids": input_ids, "attention_mask": attention_mask}
        embeddings = self.embedding_session.run(None, embedding_inputs)[0]

        # run classifier inference
        classifier_input_name = self.classifier_session.get_inputs()[0].name
        classifier_inputs = {classifier_input_name: embeddings.astype(np.float32)}
        prediction = self.classifier_session.run(None, classifier_inputs)[0]

        if as_string:
            label = SENTIMENT_MAP.get(prediction[0], "unknown")
            return label
        return prediction[0]
