from fastapi import FastAPI
# # So that all routes can access environment variables
# # dotenv loads the variables from a .env file into the system
# from dotenv import load_dotenv
# load_dotenv('.env')

from routes import base, data

app = FastAPI()

app.include_router(base.base_router)
app.include_router(data.data_router)

