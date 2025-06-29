from django.urls import path
from .views import itinerary_view

urlpatterns = [
    path('', itinerary_view, name='itinerary'),
]
