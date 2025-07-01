# apps/itinerary/services/aichat_service.py

import logging
from groq import Groq, APIConnectionError, RateLimitError, APITimeoutError, APIStatusError
from .prompt_builder import build_followup_prompt
from .prompt_builder import build_itinerary_prompt
from django.conf import settings

logger = logging.getLogger(__name__)
groq_client = Groq(api_key=settings.GROQ_API_KEY)

def get_ai_response(user_message: str, itinerary_data: str = "") -> str:
    """
    Sends user message (plus optional itinerary context) to Groq API and returns reply.
    Includes detailed error handling for connection, timeout, rate limit, and API errors.
    """
    messages = []
    if itinerary_data:
        messages.append({
            "role": "system",
            "content": build_followup_prompt(itinerary_data)
        })

    messages.append({"role": "user", "content": user_message})

    try:
        response = groq_client.chat.completions.create(
            messages=messages,
            model=settings.GROQ_MODEL
        )
        return response.choices[0].message.content

    except APIConnectionError as e:
        logger.exception("Groq API connection error")
        return "Sorry, I'm having trouble connecting to the service. Please try again shortly."

    except APITimeoutError as e:
        logger.warning("Groq API timeout")
        return "The request timed out. Could you please try again?"

    except RateLimitError as e:
        # See if retry-after header is available
        retry = getattr(e, "response", None)
        retry_after = None
        if retry is not None:
            retry_after = retry.headers.get("retry-after")
        msg = "I'm being rate-limited right now."
        if retry_after:
            msg += f" Please wait {retry_after} seconds before retrying."
        logger.warning(msg)
        return msg

    except APIStatusError as e:
        code = e.status_code
        body = getattr(e, "response", None)
        body_text = body.text if body is not None else ""
        if 500 <= code < 600:
            logger.error(f"Groq server-side error {code}: {body_text}")
            return "The service is temporarily unavailable—please try again later."
        else:
            logger.error(f"Groq API request error {code}: {body_text}")
            return "There was an issue with your request. Please check and try again."

    except Exception as e:
        logger.exception("Unexpected error with Groq API")
        return "An unexpected error occurred. Please try again in a bit."

def get_itinerary_from_weather(destination, weather_data):
    """
    Generates a travel itinerary based on forecast, with retries and detailed handling.
    """

    prompt = build_itinerary_prompt(destination, weather_data)

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=settings.GROQ_MODEL
        )
        return chat_completion.choices[0].message.content

    except APIConnectionError as e:
        logger.exception("Network issue contacting Groq API")
        return "Network issue: couldn't reach the itinerary service. Please try again."

    except APITimeoutError:
        logger.warning("Groq request timed out")
        return "Request timed out — please try again in a moment."

    except RateLimitError as e:
        # 429 error: extract retry-after from headers if available
        retry_after = getattr(e, "response", {}).headers.get("retry-after", None)
        msg = f"Rate limit reached."
        if retry_after:
            msg += f" Try again in {retry_after} seconds."
        logger.warning(msg)
        return msg

    except APIStatusError as e:
        code = e.status_code
        if 500 <= code < 600:
            logger.error(f"Groq server error {code}: {e.response.text}")
            return "Server error, please try again later."
        else:
            logger.error(f"Groq API returned {code}: {e.response.text}")
            return "There's an issue with your request—please check and try again."

    except Exception as e:
        logger.exception("Unexpected error in Groq API call")
        return "Something went wrong while generating the itinerary. Please try again later."
