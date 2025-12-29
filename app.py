from fastapi import FastAPI

from api.models.example import PredictRequest, PredictResponse
from src.sentiment_predictor import SentimentPredictor
from src.settings import Settings

settings = Settings()
app = FastAPI()
model = SentimentPredictor(
    settings.transformer_model_path, settings.classifier_model_path
)


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    prediction = model.predict(request.text)
    return PredictResponse(prediction=prediction)
