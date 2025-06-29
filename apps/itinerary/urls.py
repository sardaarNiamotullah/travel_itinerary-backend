from django.urls import path
from .views import itinerary_view, aichat_view

urlpatterns = [
    path('', itinerary_view, name='itinerary'),
    path('aichat/', aichat_view, name='ai_chat'),
]
