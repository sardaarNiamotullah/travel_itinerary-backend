from rest_framework import serializers

class ItineraryRequestSerializer(serializers.Serializer):
    destination = serializers.CharField(required=True)
    date = serializers.DateField(required=True, format="%Y-%m-%d")

    def validate_date(self, value):
        # You can add custom logic here (e.g., disallow past dates)
        return value
