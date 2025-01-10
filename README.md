# WeatherApp

# Overview
This project aims to provide users with current weather conditions such as temperature, humidity, wind speed, and overall weather description. It also provides a simple interface for users to check weather conditions by entering their location.

# Features
1. Current Weather Information
Provides personalized weather recommendations based on the current weather conditions and temperature.
Displays the current weather conditions for the specified location, including:
- Temperature
- Weather condition (e.g., Rain, Sunny, Cloudy) with Unicode icons.
- Humidity and wind speed.

2. 3-Day Weather Forecast
Displays a detailed 3-day weather forecast including:
- Date
- Minimum and maximum temperatures
- Weather condition with Unicode icons.
  
3. Hourly Weather Forecast
Provides a detailed hourly forecast for the current day, displayed horizontally in a scrollable frame.
Each hourly update includes:
- Time (in HH:MM format)
- Weather condition with Unicode icons.
- Temperature.   

4. Dynamic Weather Recommendations
Suggests actions or precautions based on current weather conditions. Examples:
- "Carry an umbrella and wear waterproof shoes" for rainy weather.
- "Stay hydrated and wear sunscreen" for hot, sunny days.
- "Wear heavy winter clothing" for cold temperatures.
  
# Limitation
1. The app fetches data provided by the WeatherAPI, which updates weather conditions periodically. This can lead to slight differences between the app's information and the real-time 
   weather.

2. App relies on how WeatherAPI resolves locations like "Bangsar" to specific coordinates. If the location resolution is too broad or inaccurate, the data might represent a nearby weather 
   station instead of the exact area.

# Dependencies
# Python Libraries:
- `os`
- `requests`
- `tkinter`
- `matplotlib`
- `re`
- External SDKs: `inference_sdk`

# APIs and Services:
WeatherAPI: For fetching current weather conditions, hourly forecasts, and 3-day forecasts.

# File Structure
- `weather_app_backend.py`: Backend logic for fetching and processing weather data.
- `weather_app.py`: GUI frontend for interacting with users. This is the main application file

# Usage
1. Install Dependencies Use the following command to install required Python libraries:
```bash
pip install requests tkinter matplotlib
```
2. Run the Application
   Start the Flask application:
```bash
python weather_app.py
```

3. Get weather location

- Enter a location in the search bar.
- View current weather, hourly forecast, and 3-day forecast.

4. Recommendations
- View weather-specific recommendations (e.g., carry an umbrella if rain is forecasted).

5. Hourly Forecast
- Scroll through the hourly weather forecast to plan your day.
  
# API Configuration
WeatherAPI
- Replace the `API_KEY` in your backend (weather_app_backend.py) with your actual WeatherAPI key.

# Code Highlights
## Weather Data Fetching (WeatherAPI)
```python
params = {
    "key": API_KEY,
    "q": location,  # User-entered location
    "days": 3,      # Number of forecast days
    "aqi": "no",    # Exclude air quality index
    "alerts": "no"  # Exclude alerts
}
response = requests.get(f"{BASE_URL}/forecast.json", params=params)
if response.status_code == 200:
    weather_data = response.json()
else:
    raise Exception(f"API call failed: {response.status_code}, {response.text}")
```
    
## Weather Recommendations
```python
def get_weather_recommendation(condition, temp):
    if "rain" in condition.lower():
        return "Carry an umbrella and wear waterproof shoes."
    elif "snow" in condition.lower():
        return "Wear warm clothes and be cautious of slippery roads."
    elif "sunny" in condition.lower() and temp > 30:
        return "Stay hydrated and wear sunscreen."
    elif "wind" in condition.lower():
        return "Secure loose items and avoid high places."
    elif temp < 5:
        return "Wear heavy winter clothing to stay warm."
    else:
        return "Weather is moderate. Enjoy your day!"
```

## Hourly Weather Forecast Parsing
```python
hourly_forecast = [
    {
        "time": hour["time"][-5:],  # Format time as HH:MM
        "temp": hour["temp_c"],
        "condition": hour["condition"]["text"]
    }
    for hour in data["forecast"]["forecastday"][0]["hour"]
]
```

# References
WeatherAPI: 
- https://www.weatherapi.com/docs/

