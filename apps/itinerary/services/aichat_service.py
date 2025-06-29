# apps/itinerary/services/aichat_service.py

from groq import Groq
from django.conf import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)

def get_ai_response(user_message):
    """
    Sends user's message to Groq API and returns assistant's reply.
    """
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model=settings.GROQ_MODEL
    )

    return chat_completion.choices[0].message.content

def get_itinerary_from_weather(destination, weather_data):
    """
    Uses Groq API to generate a travel itinerary based on weather forecast.
    """
    from .prompt_builder import build_itinerary_prompt

    prompt = build_itinerary_prompt(destination, weather_data)

    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=settings.GROQ_MODEL
    )

    return chat_completion.choices[0].message.content
