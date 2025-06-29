# apps/itinerary/services/weather_service.py

import requests
from django.conf import settings


def fetch_weather_forecast(destination):
    """
    Fetches weather forecast data for a given destination using RapidAPI.
    """
    url = "https://ai-weather-by-meteosource.p.rapidapi.com/daily"
    querystring = {
        "place_id": destination,
        "language": "en",
        "units": "auto"
    }
    headers = {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,
        "x-rapidapi-host": settings.RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")

    return response.json()
