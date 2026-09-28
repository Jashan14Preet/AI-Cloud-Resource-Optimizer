import joblib
import pandas as pd


MODEL_PATH = "models/random_forest_10min.pkl"


class PredictionService:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, workload):

        data = pd.DataFrame([workload])

        prediction = self.model.predict(data)[0]

        return {
            "cpu_usage": round(float(prediction[0]), 2),
            "memory_usage": round(float(prediction[1]), 2),
            "disk_usage": round(float(prediction[2]), 2),
            "network_usage": round(float(prediction[3]), 2)
        }


prediction_service = PredictionService()