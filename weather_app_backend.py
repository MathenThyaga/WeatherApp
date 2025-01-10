import requests
import matplotlib.pyplot as plt

# Weather API setup
API_KEY = "YOUR_ACTUAL_API_KEY"  # Replace with your WeatherAPI key
BASE_URL = "http://api.weatherapi.com/v1"

# Function to fetch weather data
def get_weather_data(location):
    url = f"{BASE_URL}/forecast.json"
    params = {
        "key": API_KEY,
        "q": location,
        "days": 3,  # Fetch data for 3 days
        "aqi": "no",
        "alerts": "no"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed: {response.status_code}, {response.text}")

# Function to parse weather data
def parse_weather_data(data):
    current = data["current"]
    forecast = data["forecast"]["forecastday"]

    current_weather = {
        "temperature": current["temp_c"],
        "condition": current["condition"]["text"],
        "humidity": current["humidity"],
        "wind_speed": current["wind_kph"]
    }

    forecast_data = []
    for day in forecast:
        forecast_data.append({
            "date": day["date"],
            "max_temp": day["day"]["maxtemp_c"],
            "min_temp": day["day"]["mintemp_c"],
            "condition": day["day"]["condition"]["text"]
        })

    return current_weather, forecast_data

# Function to parse hourly forecast data
def parse_hourly_data(data):
    hourly = data["forecast"]["forecastday"][0]["hour"]
    hourly_forecast = [
        {
            "time": hour["time"][-5:],  # Extract time in HH:MM format
            "temp": hour["temp_c"],
            "condition": hour["condition"]["text"]
        }
        for hour in hourly
    ]
    return hourly_forecast

# Function to provide weather recommendations
def get_weather_recommendation(condition, temp):
    if "rain" or "light rain" in condition.lower():
        return "Carry an umbrella and wear waterproof shoes."
    elif "snow" in condition.lower():
        return "Wear warm clothes and be cautious of slippery roads."
    elif "sunny" in condition.lower() and temp > 30:
        return "Stay hydrated and wear sunscreen."
    elif "wind" or "cloudy" or "cloudy" in condition.lower():
        return "Secure loose items and avoid high places."
    elif temp < 5:
        return "Wear heavy winter clothing to stay warm."
    else:
        return "Weather is moderate. Enjoy your day!"
