from fastapi import FastAPI

app = FastAPI(title="CapitalManager API")


@app.get("/ping")
def ping():
    """Check API is working"""
    return {"message": "pong"}
