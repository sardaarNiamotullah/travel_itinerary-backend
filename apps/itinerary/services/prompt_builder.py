def build_itinerary_prompt(destination, weather_data):
    """
    Builds a natural language prompt to generate itinerary from Groq
    based on destination and 3-day weather forecast.
    """
    forecast_lines = "\n".join(
        f"{day['day']}: {day['summary']}" for day in weather_data
    )

    # return (
    #     f"I'm traveling to {destination} for the next three days. "
    #     f"Here is the weather forecast:\n{forecast_lines}\n\n"
    #     "Can you plan a travel itinerary for these days including:\n"
    #     "- Precautions based on the weather\n"
    #     "- Suggested clothing\n"
    #     "- Local foods to try\n\n"
    #     "Make it helpful and friendly for a traveler."
    # )
    # return (        
    #     f"I'm traveling to {destination} for the next three days. "
    #     "Can you plan a travel itinerary for that day\n"

    #     "Make the response very very short and precise under 100 words max")
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
