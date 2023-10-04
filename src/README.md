The entry point for the project is the main.py where app() has been initialized.

 
Weather Recommendation:
The route for getting weather, outfit and activity summary is /weather/{city}, get_weather_city() is called for this route which is defined in weatherapis.py.
This makes call to OpenWeatherAPI and passes city as parameter. 

OpenAI API:
OpenAI API are called for generating funny summary.
Model used is text-davinci-003 from GPT-3.

Outfit Recommendation:
From weatherapi.py -> outfit_recommendation_call() is called, which return the outfit recommended. For getting recommendations DecisionTreeClassifier is used. 
Input are provided through excel sheet, which can be uploaded using API endpoint /upload(define in src> routes> crud_excel.py). There is a template defined for this in src> templates> uploadfile.html. For uploading excel the file name should be outfit_table.xlsx
Features are defined from the excel on basis of which the output i.e. recommended outfit is returned based on weather parameters.

Activity Recommendation:
For activity recommendation, get_activity_recommendation() is called from weatherapi.py whih is defined in src > sql_app> core.py
This fetches recommendation from database. Sqlite is used as the database. 
Based on weather condition the temprature, humidity and wind are classified and saved in database.
When recommendation call comes, then based on the params the value is fetched from database.

There are API endpoint for adding database entries for activity recommendation i.e. /add_activity
and to view all the entries for activity recommendations use /get_all_activity, API endpoint.
These API endpoints can be used via SwaggerUI.

In src> sql_app folder:
core.py: defines all API endpoint for adding activity recommendation and viewing them
db.py: create session and db object
models.py: Has the database model for the Activity data table.
schemas.py: Contains Pydantic schema for APIs

src> cache.py: File that defines functions for caching openweather api response, which expires after every 2 hours

To run unittest:
Unit test are defined in src> test_app.py
Go to project folder and then to src, then run
python -m unittest test_app.py


TO RUN the app,
Install virtual environment
Run the requirements.txt
provide API endpoint /weather/{city} - To view weather summar, outfit and activity recommendation

API endpoints:
/weather/{city} - To view weather summar, outfit and activity recommendation
/upload - To upload excel for outfit recommendation, this is used by DecisionTreeClassifier. Name of excel should be outfit_table.xlsx
/add_activity - To add activities for activity recommendation
/get_all_activity - To view all entries for activity recommendation
