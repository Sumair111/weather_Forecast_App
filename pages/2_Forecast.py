import streamlit as st
import requests
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

API_KEY = "6a4b3c928751d3a5640787f17d805d62"  # Replace with your real API key

st.title("🌦️ Predicted Weather upto 5 Days")
city_name = st.text_input("Enter City Name")

# Function to plot hourly forecast
def plot_hourly_forecast(data):
    # Extract hours and temperatures
    hours = [entry["dt_txt"].split(" ")[1][:5] for entry in data["list"]]
    temps = [entry["main"]["temp"] for entry in data["list"]]
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(hours, temps, marker='o', color='tab:blue')
    plt.title('Hourly Temperature Forecast')
    plt.xlabel('Hour of Day')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Display the plot
    st.pyplot(plt)

if city_name:
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    if response.status_code==200:
        data = response.json()
        

    if "list" in data:
        st.subheader(f"📍 Forecast for {data['city']['name']}, {data['city']['country']}")
        
        # Group forecast data by date
        forecast_by_date = defaultdict(list)
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            forecast_by_date[date].append(entry)

        # Show forecasts per day
        for date, entries in forecast_by_date.items():
            st.markdown(f"### 📅 {date}")
            for entry in entries:
                time = entry["dt_txt"].split(" ")[1][:5]
                temp = entry["main"]["temp"]
                weather = entry["weather"][0]["description"].title()
                wind = entry["wind"]["speed"]
                st.write(f"🕒 {time} | 🌡️ {temp}°C | 🌥️ {weather} | 💨 Wind: {wind} m/s")
            plot_hourly_forecast({"list":entries})
            st.markdown("---")
    else:
        st.error("Could not fetch forecast data.")
        




