import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import weatherapis
from routes import crud_excel
from sql_app import core 


app = FastAPI()

# NEW
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(weatherapis.router)
app.include_router(crud_excel.router)
app.include_router(core.router)

os.environ['WEATHER_API_KEY'] = '5f5cfef0e951d155025a26e184c7dcd2'
os.environ['OPENAI_API_KEY'] = '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'

@app.get("/")
def home():
    return "Welcome! For weather information got to /weather/{city_name}"