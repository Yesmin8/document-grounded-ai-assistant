from fastapi import FastAPI

app = FastAPI(
    title="Document Grounded AI Assistant",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Backend is running"
    }
