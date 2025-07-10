# main.py

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routes import analyze_routes

app = FastAPI()

# MongoDB Setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["CasteGuardDB"]  # Replace with your DB name

# Inject DB into router
app.include_router(analyze_routes.router, prefix="/api", tags=["analyze"])
app.state.mongo = db
