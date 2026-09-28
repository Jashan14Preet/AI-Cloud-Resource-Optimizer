from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.prediction import router as prediction_router
from app.api.result_api import router as result_router


app = FastAPI(
    title="AI Cloud Resource Optimizer",
    description=(
        "AI-Based Predictive Resource Allocation "
        "for Energy-Efficient Cloud Infrastructure"
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    prediction_router
)

app.include_router(
    result_router
)


@app.get("/")
def root():

    return {
        "message":
        "AI Cloud Resource Optimizer API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }