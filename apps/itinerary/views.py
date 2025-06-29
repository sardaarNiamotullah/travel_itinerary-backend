from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ItineraryRequestSerializer, AIChatRequestSerializer
from .services.weather_service import fetch_weather_forecast
from .services.aichat_service import get_ai_response, get_itinerary_from_weather


@api_view(['POST'])
def itinerary_viewd(request):
    """
    Handles POST requests to /api/itinerary.
    Expects JSON with 'destination' and 'date'.
    Returns weather info for 3 consecutive days starting from the given date.
    """

    serializer = ItineraryRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    destination = serializer.validated_data['destination']
    date = serializer.validated_data['date'].isoformat()  # e.g. "2025-07-15"

    try:
        weather_data = fetch_weather_forecast(destination)
        daily_data = weather_data.get('daily', {}).get('data', [])

        start_index = next(
            (i for i, day in enumerate(daily_data) if day.get('day') == date),
            None
        )

        if start_index is None:
            return Response({'message': f"No weather data found for {date}"}, status=status.HTTP_404_NOT_FOUND)

        three_days = daily_data[start_index:start_index + 3]

        return Response(three_days, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def aichat_view(request):
    """
    Handles POST /api/itinerary/aichat/
    Sends 'message' to Groq API and returns the response.
    """
    serializer = AIChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_message = serializer.validated_data['message']

    try:
        ai_reply = get_ai_response(user_message)
        return Response({"reply": ai_reply}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def itinerary_view(request):
    serializer = ItineraryRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    destination = serializer.validated_data['destination']
    date = serializer.validated_data['date'].isoformat()

    try:
        weather_data = fetch_weather_forecast(destination)
        daily_data = weather_data.get('daily', {}).get('data', [])

        # Find the index of the day matching the requested date
        start_index = next(
            (i for i, day in enumerate(daily_data) if day.get('day') == date),
            None
        )

        if start_index is None:
            return Response({'message': f"No weather data found for {date}"}, status=status.HTTP_404_NOT_FOUND)

        # Get 3-day forecast
        three_days = daily_data[start_index:start_index + 3]

        # Generate AI-based travel suggestion using Groq
        itinerary_suggestion = get_itinerary_from_weather(destination, three_days)

        return Response({
            "ai_itinerary": itinerary_suggestion,
            "forecast": three_days
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)