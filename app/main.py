from fastapi import FastAPI
import os
app = FastAPI(
    title="Devops Entry Project",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to dhruvil DevOps Project"
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
