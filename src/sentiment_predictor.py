import joblib
from sentence_transformers import SentenceTransformer


class SentimentPredictor:
    def __init__(self, transformer_path: str, logreg_path: str):
        self.transformer = SentenceTransformer(transformer_path)
        self.logreg = joblib.load(logreg_path)

    def predict(self, text: str, as_string: bool = True) -> int | str:
        if not text or not isinstance(text, str):
            raise ValueError("Input text is empty")

        embedding = self.transformer.encode([text])
        prediction = self.logreg.predict(embedding)
        if as_string:
            prediction = self.__map_to_string(prediction)
        return prediction

    def __map_to_string(self, prediction: int) -> str:
        match prediction:
            case 0:
                return "negative"
            case 1:
                return "neutral"
            case 2:
                return "positive"
            case _:
                raise ValueError(f"Unexpected prediction: {prediction}")
