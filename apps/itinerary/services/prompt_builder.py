def build_itinerary_prompt(destination, weather_data):
    """
    Builds a natural language prompt to generate itinerary from Groq
    based on destination and 3-day weather forecast.
    """
    forecast_lines = "\n".join(
        f"{day['day']}: {day['summary']}" for day in weather_data
    )

    return (
        f"I'm traveling to {destination} for the next three days. "
        f"Here is the weather forecast:\n{forecast_lines}\n\n"
        "Can you plan a travel itinerary for these days including:\n"
        "- Precautions based on the weather\n"
        "- Suggested clothing\n"
        "- Local foods to try\n\n"
        "Make it helpful and friendly for a traveler.\n\n"
        "Your Response shoud fllow this manner [[Day 1 data],[Day 2 data],[Day 3 data],] i.e one parent array and 3 child array inside of it containing the initiraty about each day. \n\n"
        "DO NOT RESPONSE WITH ANYTHING OUTSIE OF ARRAY."
    )

def build_followup_prompt(itinerary_data: str) -> str:
    """
    Builds the system message for follow-up AI conversation based on itinerary context.
    """
    return (
        "The user has shared the following itinerary data. "
        "Keep this context in mind when replying:\n\n"
        f"{itinerary_data}\n\n"
        "Be very precise and on the point. However, sound friendly at the same time."
    )

