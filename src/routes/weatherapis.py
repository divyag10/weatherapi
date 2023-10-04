from fastapi import APIRouter, Depends, Query
import cache
import requests
import http
import httpx
from httpx import Response
import os
import openai

import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from pathlib import Path
from sql_app.core import get_activity_recommendation



router = APIRouter()


def _report_url(city: str, weather_api_key: str):
    return (
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}')


def open_ai_call(prompt_val: str):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_val,
        max_tokens=60,
        temperature=0.5
        )
    summary = response.choices[0].text.strip()
    return summary

def outfit_recommendation_call(temperature: float, wind: float, humidity: float):
    script_dir = Path(__file__).resolve().parent
    xls_data_path = script_dir / 'outfit_table.xlsx'

    read_file = pandas.DataFrame(pandas.read_excel(xls_data_path))
    read_file.to_csv ("outfit_csv.csv", 
                      index = None,
                      header=True)
    
    csv_file = 'outfit_csv.csv'
    df = pandas.read_csv(csv_file)
    d = {'multiple layers': 0, 'Cottons': 1, 'Breathable fabrics': 2, 'denims': 3}
    df['recommendation'] = df['recommendation'].map(d)

    features = ['temperature', 'humidity', 'wind']
    X = df[features]
    y = df['recommendation']
    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(X, y)
    recomm = dtree.predict([[temperature, humidity, wind]])
    outfit_recomm = {i for i in d if d[i]==recomm}
    outfit_val = next(iter(outfit_recomm))
    return outfit_val


@router.get("/weather/{city}")
async def get_weather_city(city: str):
    
    #fetch data from OPENWEATHERMAP API
    weather_api_key = os.environ['WEATHER_API_KEY']

    #check if cache has weather data from last 12 hours
    forecast = cache.get_weather(city)
    if not forecast:
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(
                url=_report_url(city, weather_api_key)
            )
            if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
                raise ValidationError(response.text, response.status_code)
        forecast = response.json()
        #set the weather information in cache
        cache.set_weather(city, forecast)

    #fetch relevant data from weather API response
    temperature_kelvin = forecast['main']['temp']
    temperature = round(temperature_kelvin - 273.15, 2)
    wind = forecast['wind']['speed']
    humidity = forecast['main']['humidity']
    temperature_feel = forecast['main']['feels_like']


    weather_prompt =f"OpenAI, give me a funny summary for "+ str(temperature) +" degree celsius temperature with humidity "+ str(humidity) +" percentage and "+ str(wind) +" meters/sec wind speed.Also, don't mention stats in summary please"
    #OPEN AI call for weather summary
    weather_summary = open_ai_call(weather_prompt)

    #fetch outfit recommendation
    outfit_recommdation = outfit_recommendation_call(temperature, wind, humidity)
    print('*****Outfit recommended is*******'+outfit_recommdation)
    #OPEN AI call for outfit summary
    outfit_prompt = "Suggest in a line "+outfit_recommdation+" as outfit for the day, given the temperature is "+ str(temperature)+" and humidity is "+str(humidity)
    outfit_summary = open_ai_call(outfit_prompt)

    #fetch activity recommendation
    activity_recommendation = get_activity_recommendation(temperature, wind, humidity)
    print('******Activity recommendation is***** '+ activity_recommendation)
    activity_prompt = "Suggest in a line activity for the day as "+activity_recommendation+" ,given the temprature is "+ str(temperature)+" and humidity is "+str(humidity)
    activity_summary = open_ai_call(activity_prompt)

    return{'city': city, 'weather_summary': weather_summary,'activity_recommendation': activity_summary,'outfit_recommdation': outfit_summary}
    

    



    

        

