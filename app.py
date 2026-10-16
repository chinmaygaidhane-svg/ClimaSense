import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

st.title("ClimaSense")
st.write("Enter the city Name and click the button to fetch the weather data")

city_name = st.text_input("Enter city name", value="Nagpur")

if st.button("Get Weather Data"):
    if not city_name.strip():
        st.warning("Please enter a city name.")
    else:
        api_key = os.getenv("WEATHER_API_KEY")  # Ensure this matches your .env variable name
        
        if not api_key:
            st.error("API key not found! Check your .env file.")
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name.strip()}&appid={api_key}&units=metric"
            
            try:
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    city = data.get("name")
                    country = data.get("sys", {}).get("country", "")
                    temp = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    wind = data["wind"]["speed"]
                    condition = data["weather"][0]["description"]

                    st.subheader(f"{city}, {country}")

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Temperature 🌡️", f"{temp} °C")
                    col2.metric("Humidity 💧", f"{humidity}%")
                    col3.metric("Wind Speed 💨", f"{wind} m/s")
                    col4.metric("Condition 🌤️", condition.title())
                else:
                    # Shows the exact error message from the API (e.g. invalid key, city not found)
                    st.error(f"Error ({response.status_code}): {data.get('message', 'Failed to fetch data')}")

            except Exception as e:
                st.error(f"Request failed: {e}")