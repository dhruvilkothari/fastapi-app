from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import os

app = FastAPI(
    title="Devops Entry Project",
    version="1.0.0"
)

# Enable Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
def home():
    return {
        "message": "Welcome to dk DevOps Project"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/api/v1/info")
def application_info():
    return {
        "application": "FastAPI DevOps Project",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development")
    }