# from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # disable CSRF just for simplicity (not for production)
def itinerary_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            destination = data.get('destination')
            date = data.get('date')
            return JsonResponse({
                'message': f'We have got your destination ({destination}) and date ({date}).'
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
