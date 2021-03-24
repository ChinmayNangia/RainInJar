import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient
API_KEY = os.environ.get("OWM_API_KEY")
OWN_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
MY_LAT = 43.653225
MY_LONG = -79.383186
account_sid = os.environ.get("TwillioSID")
auth_token = os.environ.get("Twilio_Auth_token")

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}
response = requests.get(OWN_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It is going to rain today,Remember to bring umbrella ☔",
        from_ ='from the number given by twilio dashboard',
        to='Your verified number on twilio'
    )
    print(message.status)

