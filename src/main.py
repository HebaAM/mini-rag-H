from fastapi import FastAPI
# # So that all routes can access environment variables
# # dotenv loads the variables from a .env file into the system
# from dotenv import load_dotenv
# load_dotenv('.env')

from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app_settings = get_settings()
    app.mongodb_connection = AsyncIOMotorClient(app_settings.MONGODB_URL)
    app.db_client = app.mongodb_connection[app_settings.MONGODB_DB]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connection.close()


app.include_router(base.base_router)
app.include_router(data.data_router)

