import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
print(f"DEBUG: Using API Key -> {API_KEY}") 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# Weather condition icons
WEATHER_ICONS = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
    'fog': '🌫️',
    'haze': '🌫️'
}

def get_weather_icon(description):
    """Returns an emoji icon based on weather description"""
    for condition, icon in WEATHER_ICONS.items():
        if condition in description.lower():
            return icon
    return '🌈'

def get_weather(city_name):
    """Fetches weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'  # Use 'imperial' for Fahrenheit
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        
        weather_data = response.json()
        
        return {
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'pressure': weather_data['main']['pressure'],
            'city': weather_data['name'],
            'country': weather_data['sys']['country']
        }
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print("City not found. Please check the name and try again.")
        else:
            print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError:
        print("Network error. Please check your internet connection.")
        return None
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        return None

def display_weather(weather):
    """Displays weather information in a user-friendly format"""
    if weather:
        print("\n🌦️ Weather Information 🌦️")
        print("──────────────────────────")
        print(f"📍 {weather['city']}, {weather['country']}")
        print(f"{get_weather_icon(weather['description'])} {weather['description'].capitalize()}")
        print(f"🌡️ Temperature: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)")
        print(f"💧 Humidity: {weather['humidity']}%")
        print(f"🌬️ Wind Speed: {weather['wind_speed']} m/s")
        print(f"⏲️ Pressure: {weather['pressure']} hPa")
        print("──────────────────────────")
    else:
        print("No weather data to display.")

def main():
    """Main function to run the weather application"""
    print("\nWelcome to the Python Weather App!")
    print("Get current weather conditions for any city worldwide.")
    print("Type 'quit' or 'exit' to end the program.\n")
    
    while True:
        city = input("Enter city name: ").strip()
        
        if city.lower() in ('quit', 'exit'):
            print("\nThank you for using the Weather App. Goodbye! 👋")
            break
            
        weather = get_weather(city)
        display_weather(weather)

if __name__ == "__main__":
    main()