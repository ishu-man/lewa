from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def health_check():
    return {"message": "The API is active."}