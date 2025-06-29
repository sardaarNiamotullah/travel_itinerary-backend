# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from .services.weather_service import fetch_weather_forecast


# @api_view(['POST'])
# def itinerary_view(request):
#     """
#     Handles POST requests to /api/itinerary.
#     Expects JSON with 'destination' and 'date'.
#     Returns weather info for 3 consecutive days starting from the given date.
#     """
#     destination = request.data.get('destination')
#     date = request.data.get('date')

#     if not destination or not date:
#         return Response({'error': 'Destination and date are required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         weather_data = fetch_weather_forecast(destination)
#         daily_data = weather_data.get('daily', {}).get('data', [])

#         # Find the index of the day matching the requested date
#         start_index = next(
#             (i for i, day in enumerate(daily_data) if day.get('day') == date),
#             None
#         )

#         if start_index is None:
#             return Response({'message': f"No weather data found for {date}"}, status=status.HTTP_404_NOT_FOUND)

#         # Return up to 3 consecutive days
#         three_days = daily_data[start_index:start_index + 3]

#         return Response(three_days, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ItineraryRequestSerializer
from .services.weather_service import fetch_weather_forecast


@api_view(['POST'])
def itinerary_view(request):
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
