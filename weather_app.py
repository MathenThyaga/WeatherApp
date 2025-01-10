import tkinter as tk
from tkinter import messagebox, ttk, Scrollbar, Canvas
from weather_app_backend import get_weather_data, parse_weather_data, parse_hourly_data, get_weather_recommendation

# Function to get weather icons based on condition
def get_weather_icon(condition):
    if "rain" in condition.lower():
        return "\u2614"  # Unicode for umbrella with raindrops
    elif "cloud" in condition.lower() or "overcast" in condition.lower():
        return "\u2601"  # Unicode for cloud
    elif "sun" in condition.lower() or "clear" in condition.lower():
        return "\u2600"  # Unicode for sun
    elif "wind" in condition.lower():
        return "\ud83c\udf2c"  # Unicode for wind
    elif "snow" in condition.lower():
        return "\u2744"  #Unicode for snow
    else:
        return "\u2753"  # Unicode for question mark (default)

# Function to display weather information
def display_weather():
    location = location_entry.get()
    if not location.strip():
        messagebox.showerror("Error", "Please enter a location.")
        return

    try:
        data = get_weather_data(location)
        current_weather, forecast = parse_weather_data(data)
        hourly_data = parse_hourly_data(data)

        # Display current weather
        current_weather_label.config(
            text=(f"Location: {location}\n"
                  f"Temperature: {current_weather['temperature']}°C\n"
                  f"Condition: {get_weather_icon(current_weather['condition'])} {current_weather['condition']}\n"
                  f"Humidity: {current_weather['humidity']}%\n"
                  f"Wind Speed: {current_weather['wind_speed']} km/h\n\n"
                  f"Recommendation: {get_weather_recommendation(current_weather['condition'], current_weather['temperature'])}")
        )

        # Clear old hourly content
        for widget in hourly_forecast_frame.winfo_children():
            widget.destroy()

        # Display hourly forecast horizontally in a scrollable frame
        for hour in hourly_data:
            hour_frame = tk.Frame(hourly_forecast_frame, bg="#8fa9e3", padx=10, pady=10)
            hour_frame.pack(side="left", padx=5, pady=5)

            hour_label = tk.Label(
                hour_frame,
                text=(f"Time: {hour['time']}\n"
                      f"{get_weather_icon(hour['condition'])} {hour['condition']}\n"
                      f"Temp: {hour['temp']}°C"),
                font=("Arial", 10),
                bg="#8fa9e3"
            )
            hour_label.pack()

        # Update 3-day forecast
        for i, day in enumerate(forecast):
            forecast_labels[i].config(
                text=(f"{get_weather_icon(day['condition'])} {day['date']}\n"
                      f"Condition: {day['condition']}\n"
                      f"Min Temp: {day['min_temp']}°C\n"
                      f"Max Temp: {day['max_temp']}°C")
            )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")

# Initialize the main window
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("1000x800")
root.configure(bg="#d9e7ff")

# Title
title_label = tk.Label(root, text="Weather Dashboard", font=("Arial", 24, "bold"), bg="#5d79a3", fg="white", pady=10)
title_label.pack(fill="x")

# Search Frame
search_frame = tk.Frame(root, bg="#d9e7ff", pady=10)
search_frame.pack()

location_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
location_entry.pack(side="left", padx=10)

search_button = tk.Button(search_frame, text="Search", font=("Arial", 14), command=display_weather)
search_button.pack(side="left")

# Current Weather
current_weather_label = tk.Label(root, text="", font=("Arial", 14), bg="#d9e7ff", justify="left", wraplength=800)
current_weather_label.pack(pady=10)

# Hourly Forecast Section
forecast_title = tk.Label(root, text="Hourly Forecast", font=("Arial", 16, "bold"), bg="#d9e7ff", pady=10)
forecast_title.pack()

hourly_frame = tk.Frame(root, bg="#d9e7ff")
hourly_frame.pack(pady=10, fill="x")

hourly_canvas = Canvas(hourly_frame, bg="#d9e7ff", height=150)
hourly_canvas.pack(side="top", fill="both", expand=True)

hourly_forecast_frame = tk.Frame(hourly_canvas, bg="#d9e7ff")
hourly_forecast_frame.bind(
    "<Configure>", lambda e: hourly_canvas.configure(scrollregion=hourly_canvas.bbox("all"))
)

hourly_canvas.create_window((0, 0), window=hourly_forecast_frame, anchor="nw")

# Centered horizontal scrollbar
hourly_scrollbar = Scrollbar(root, orient="horizontal", command=hourly_canvas.xview)
hourly_scrollbar.pack(side="top", fill="x", padx=20)
hourly_canvas.configure(xscrollcommand=hourly_scrollbar.set)

# 3-Day Forecast Section
forecast_title = tk.Label(root, text="3 Day Forecast", font=("Arial", 16, "bold"), bg="#d9e7ff", pady=10)
forecast_title.pack()

forecast_frame = tk.Frame(root, bg="#d9e7ff", pady=20)
forecast_frame.pack()

forecast_labels = [
    tk.Label(forecast_frame, text="", font=("Arial", 12), bg="#8fa9e3", padx=10, pady=10, width=30, height=8, wraplength=200)
    for _ in range(3)
]

for label in forecast_labels:
    label.pack(side="left", padx=10, pady=10)

root.mainloop()
