from datetime import date, timedelta
from rest_framework import serializers

class ItineraryRequestSerializer(serializers.Serializer):
    destination = serializers.CharField(required=True)
    date = serializers.DateField(required=True, format="%Y-%m-%d")

    def validate_date(self, value):
        today = date.today()
        max_allowed_date = today + timedelta(days=15)

        if value < today:
            raise serializers.ValidationError("Date cannot be in the past.")
        if value > max_allowed_date:
            raise serializers.ValidationError("Date cannot be more than 15 days from today.")
        return value

class AIChatRequestSerializer(serializers.Serializer):
    itinerary_data = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField(required=True, help_text="Your message to the AI")

