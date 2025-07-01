import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class WeatherServiceError(Exception):
    """Base exception for weather service errors."""
    pass

class WeatherServiceTimeout(WeatherServiceError):
    """Timeout occurred."""
    pass

class WeatherServiceAPIError(WeatherServiceError):
    """API returned an error response."""
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code}: {detail}")

def fetch_weather_forecast(destination: str, timeout: int = 10) -> dict:
    """
    Fetches daily weather forecast data for a given destination using RapidAPI (Meteosource).
    Raises WeatherServiceError on failure.
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

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=timeout)

    except requests.Timeout as e:
        logger.error("Timeout while calling Meteosource API", exc_info=e)
        raise WeatherServiceTimeout("Weather request timed out. Please try again later.")

    except requests.RequestException as e:
        logger.error("Network error when calling Meteosource API", exc_info=e)
        raise WeatherServiceError("Network error occurred. Please try again later.")

    if response.status_code != 200:
        try:
            data = response.json()
            detail = data.get("detail") or data.get("message") or response.text
        except ValueError:
            detail = response.text

        logger.error(
            "Meteosource API error: status=%s, detail=%s",
            response.status_code, detail
        )
        raise WeatherServiceAPIError(response.status_code, detail)

    try:
        return response.json()
    except ValueError as e:
        logger.error("Failed to parse Meteosource API JSON", exc_info=e)
        raise WeatherServiceError("Invalid response format from weather service.")
