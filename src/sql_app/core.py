from .schemas import ActivityDataSchema, DeleteActivitySchema
from .models import ActivityData
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .db import get_db, Base, engine, get_session
from typing import List
from . import models
from sqlalchemy import and_	



router = APIRouter()

models.Base.metadata.create_all(bind=engine)

def get_weather_vals(temperature, humidity, wind):
	weather_str = 'cold' if temperature < 0 else 'mild' if temperature < 22 else 'warm' if temperature < 32 else 'hot'
	humidity_str = 'low' if humidity <40 else 'moderate' if humidity <70 else 'high'
	wind_str = 'gentle' if wind <7 else 'moderate' if wind < 9 else 'strong' if wind < 11 else 'very strong'
	return weather_str, humidity_str, wind_str


@router.post('/add_activity', response_model=ActivityDataSchema)
def add_activity(a1: ActivityDataSchema, db: Session = Depends(get_db)):
	weather_val, humidity_val, wind_val = get_weather_vals(a1.temperature, a1.humidity, a1.wind)
	activity=ActivityData(id=a1.id, temperature=a1.temperature, humidity=a1.humidity, wind=a1.wind,
		recommendation=a1.recommendation, weather=weather_val, humidity_val=humidity_val, wind_val=wind_val)
	db.add(activity)
	db.commit()
	db.refresh(activity)
	return ActivityData(**a1.dict())


@router.get('/get_all_activity')
def get_activity(db: Session = Depends(get_db)):
	recs = db.query(ActivityData).all()
	return recs


def get_filtered_activity(weather_str, humidity_str, wind_str):
	session = get_session()
	print('Vals are: '+weather_str + humidity_str + wind_str)
	recs = session.query(ActivityData).filter(and_(ActivityData.weather==weather_str, ActivityData.humidity_val==humidity_str,
		ActivityData.wind_val==wind_str)).first()
	if recs != None:
		return recs.recommendation
	else:
		return ''


def get_activity_recommendation(temperature, humidity, wind):
	weather_val, humidity_val, wind_val = get_weather_vals(temperature, humidity, wind)
	activity_recommendation = get_filtered_activity(weather_val, humidity_val, wind_val)
	return activity_recommendation




