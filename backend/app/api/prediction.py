from fastapi import APIRouter
from app.services.prediction_service import prediction_service


router = APIRouter(
    prefix="/api/prediction",
    tags=["Prediction"]
)


@router.post("/predict")
def predict_workload(workload: dict):

    prediction = prediction_service.predict(workload)

    return {
        "prediction_horizon": "10 minutes",
        "predicted_workload": prediction
    }