## [Click Here](https://github.com/sardaarNiamotullah/travel_itinerary-backend) to see the github repo


## ✈️ Travel Itinerary – Backend
This Django project provides a RESTful API that delivers real-time and AI-enhanced weather data. It fetches weather forecasts from the Meteosource Weather API via RapidAPI, and integrates with the Groq API to enhance responses with AI-generated insights.

To use this application, you'll need to obtain API keys from the following services:

## 🔑 Required API Keys

### Meteosource Weather API via RapidAPI

- Visit: [RapidAPI - Meteosource](https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/playground/apiendpoint_051aea00-95fb-437c-944c-06dd8d4049d8)

- Create a RapidAPI account if you don't have one.

- Subscribe to the API and copy your X-RapidAPI-Key.

### Groq API (for AI features)

- Visit: [Groq Console](https://console.groq.com/keys)
- Sign up or log in.
- Generate an API key.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ 
- Django 3+
- pip 24+

### Installation

1. **Clone the repository**
   ```bash
   https://github.com/sardaarNiamotullah/travel_itinerary-backend.git
   cd travel_itinerary-backend.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   # If this do not work then try with this
   python3 -m venv env
   # Now activate it
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt # or pip3 install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   pip install -r requirements.txt # or pip3 install -r requirements.txt

   RAPIDAPI_KEY=your-rapid-api-key
   RAPIDAPI_HOST=ai-weather-by-meteosource.p.rapidapi.com

   GROQ_API_KEY=Your-groq-api-key
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

5. **Run the development server** 
   ```bash
   python manage.py runserver
   ```

5. **🚚 Deployment** 
   ```bash
   gunicorn your_project_name.wsgi:application
   ```



## Contributing

Got an idea to make it even better? Fork it, code it, and create a PR — contributions are **always welcome**!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🖋️ Author

**Sardaar Niamotullah**

## Acknowledgments

- Django – The high-level Python web framework.
- Django REST Framework – Powerful and flexible toolkit for building Web APIs.
- django-cors-headers – For handling Cross-Origin Resource Sharing (CORS).
- Groq – AI API used for generating smart responses.
- Gunicorn – Python WSGI HTTP server for production deployment.
- httpx – A modern, fully featured HTTP client for Python.
- python-decouple – For managing environment variables.
- Pydantic – Data validation and settings management using Python type annotations.
- Requests – Simple HTTP library for Python, used for making external API calls.