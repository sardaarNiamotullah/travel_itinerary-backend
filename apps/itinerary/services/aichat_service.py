# apps/itinerary/services/aichat_service.py

from groq import Groq
from django.conf import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)

def get_ai_response(user_message, itinerary_data=""):
    """
    Sends user's message and optional itinerary context to Groq API and returns the reply.
    """
    messages = []

    if itinerary_data:
        messages.append({
            "role": "system",
            "content": f"The user has shared the following itinerary data. Keep this context in mind when replying:\n\n{itinerary_data}"
        })

    messages.append({
        "role": "user",
        "content": user_message
    })

    chat_completion = groq_client.chat.completions.create(
        messages=messages,
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
