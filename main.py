import os
from fastapi import FastAPI

app = FastAPI()

APP_VERSION = os.getenv("APP_VERSION", "v2.0.0")

@app.get("/")
def read_root():
    return {"status": "healthy", "version": APP_VERSION, "message": "Hello from FastAPI on K8s!"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}