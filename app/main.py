from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return { "message": "Welcome to FastAPI"}

@app.get("/hello")
async def welcome() -> dict:
    return { "message": "Hello, World!"}

