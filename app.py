import onnxruntime as ort
from fastapi import FastAPI
from mangum import Mangum
from tokenizers import Tokenizer

from api.models.example import PredictRequest, PredictResponse
from src.scripts.settings import Settings
from src.sentiment_predictor import SentimentPredictor

settings = Settings()
tokenizer = Tokenizer.from_file(settings.onnx_tokenizer_path)
ort_session = ort.InferenceSession(settings.onnx_embedding_model_path)
ort_classifier = ort.InferenceSession(settings.onnx_classifier_path)

app = FastAPI()
model = SentimentPredictor(tokenizer, ort_session, ort_classifier)

handler = Mangum(app)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    prediction = model.predict(request.text)
    return PredictResponse(prediction=prediction)
