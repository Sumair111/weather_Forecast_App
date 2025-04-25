import json
import requests 
import streamlit as st
import datetime

# Your OpenWeather API key
API_KEY = "6a4b3c928751d3a5640787f17d805d62"

# Function to get weather data
def get_weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather = {
            "City Name": data["name"],
            "Country": data["sys"]["country"], 
            "Weather": data["weather"][0]["description"].title(),
            "Temperature(C)": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Pressure(hpa)": data["main"]["pressure"],
            "Wind Speed": data["wind"]["speed"],
            "Feels Like": data["main"]["feels_like"]
        }
        return weather
    else:
        return None

# Streamlit UI
st.title("🌤️ Weather Forecast App")
st.markdown("Get real-time weather updates from any city")

# Take user input
city_name = st.text_input("Enter City Name:")

# Show result if user enters a city
if city_name:
    weather_data = get_weather(city_name)

    if weather_data:
        st.success(f"Weather in {weather_data['City Name']}, {weather_data['Country']}")
        st.metric("Temperature (C)", f"{weather_data['Temperature(C)']} °C")
        st.write(f"**Weather:** {weather_data['Weather']}")
        st.write(f"**Humidity:** {weather_data['Humidity']}%")
        st.write(f"**Pressure:** {weather_data['Pressure(hpa)']} hPa")
        st.write(f"**Wind Speed:** {weather_data['Wind Speed']} m/s")
        st.write(f"**Feels Like:** {weather_data['Feels Like']} °C")
    else:
        st.error("City not found. Please try again.")
