
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from html import escape

# ==================== CONFIGURATION ====================
load_dotenv()

st.set_page_config(
    page_title="ClimaSense | Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #08111d, #101c2a, #172438);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    height: 0;
    background: transparent;
}

.block-container {
    max-width: 1450px;
    padding-top: 0.6rem;
    padding-bottom: 1.5rem;
}

#MainMenu, footer {
    visibility: hidden;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.8rem;
}

.brand {
    color: #7dd3fc;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-heading {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 6px;
}

.hero-subtitle {
    color: #a7bbd1;
    font-size: 14px;
    line-height: 1.6;
}

.search-panel {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 15px;
    padding: 10px 16px 4px 16px;
    margin: 8px 0 12px 0;
}

.stTextInput label {
    color: #dceafa !important;
    font-weight: 600;
    font-size: 13px;
}

.stTextInput input {
    background: #111f30 !important;
    color: white !important;
    border: 1px solid #344b65 !important;
    border-radius: 10px !important;
    min-height: 40px;
}

.stButton > button {
    background: linear-gradient(100deg, #38bdf8, #60a5fa);
    color: #07111f !important;
    font-weight: 800;
    border: none;
    border-radius: 10px;
    min-height: 40px;
    width: 100%;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
}

.section-title {
    color: #ffffff;
    font-size: 21px;
    font-weight: 750;
    margin: 10px 0 12px 0;
    padding: 0;
    line-height: 1.4;
}

.weather-hero {
    background: linear-gradient(125deg, #1c344b, #142438 65%, #102035);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 22px;
    padding: 25px;
    min-height: 270px;
    height: 100%;
    box-sizing: border-box;
    box-shadow: 0 15px 45px rgba(0,0,0,0.16);
}

.location-name {
    color: white;
    font-size: clamp(25px, 3vw, 36px);
    font-weight: 800;
    overflow-wrap: anywhere;
}

.country-code {
    color: #38bdf8;
    font-size: 17px;
    font-weight: 600;
}

.local-time {
    color: #a7bbd1;
    font-size: 12px;
    margin-top: 8px;
}

.temperature {
    color: white;
    font-size: clamp(65px, 7vw, 90px);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -4px;
    margin-top: 18px;
}

.weather-condition {
    color: #c4ddf4;
    font-size: 17px;
    margin-top: 5px;
}

.feels-like {
    display: inline-block;
    color: #d8eafa;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 7px 12px;
    border-radius: 20px;
    margin-top: 15px;
    font-size: 12px;
}

.sky-card {
    background: linear-gradient(145deg, #172b40, #111e30);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 22px;
    padding: 24px;
    min-height: 270px;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.sky-icon {
    font-size: 76px;
    margin: 15px 0;
}

.sky-caption {
    color: #8ca9c6;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.sky-description {
    color: white;
    font-size: 21px;
    font-weight: 700;
}

.metric-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 17px;
    min-height: 125px;
    height: 100%;
    box-sizing: border-box;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: #38bdf8;
}

.metric-icon {
    font-size: 22px;
    margin-bottom: 9px;
}

.metric-label {
    color: #9eb4cb;
    font-size: 12px;
    margin-bottom: 7px;
}

.metric-value {
    color: white;
    font-size: 22px;
    font-weight: 750;
    overflow-wrap: anywhere;
}

.advisory-card {
    background: linear-gradient(145deg, #141f2b, #101722);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 17px;
    padding: 19px;
    min-height: 175px;
    height: 100%;
    box-sizing: border-box;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.advisory-card:hover {
    transform: translateY(-4px);
    border-color: #38bdf8;
}

.advisory-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}

.advisory-icon {
    font-size: 27px;
}

.advisory-title {
    color: white;
    font-size: 15px;
    font-weight: 750;
}

.advisory-status {
    color: #7dd3fc;
    font-size: 11px;
    margin-top: 5px;
}

.advisory-description {
    color: #bdcddd;
    font-size: 12px;
    line-height: 1.7;
}

.footer {
    border-top: 1px solid rgba(255,255,255,0.10);
    margin-top: 28px;
    padding-top: 17px;
    color: #8298b0;
    font-size: 11px;
    text-align: center;
}

@media (max-width: 700px) {
    .weather-hero, .sky-card {
        padding: 20px;
        min-height: 240px;
    }

    .temperature {
        letter-spacing: -3px;
    }

    .advisory-card {
        min-height: auto;
    }

    .section-title {
        font-size: 19px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================== HEADER ====================
st.markdown("""
<div class="brand">✦ CLIMASENSE · WEATHER INTELLIGENCE</div>
<div class="hero-heading">
    Weather, <span style="color:#7dd3fc;">reimagined.</span>
</div>
<div class="hero-subtitle">
    Explore current weather conditions and get practical
    recommendations for your day.
</div>
""", unsafe_allow_html=True)


# ==================== CITY SEARCH ====================
st.markdown('<div class="search-panel">', unsafe_allow_html=True)

search_col, button_col = st.columns([4, 1], gap="medium")

with search_col:
    city_name = st.text_input(
        "Search destination",
        value="Nagpur",
        placeholder="Enter a city, e.g. Pune, Tokyo or London"
    )

with button_col:
    # Align the button with the text input, without an extra spacer.
    st.markdown(
        '<div style="height:27px"></div>',
        unsafe_allow_html=True
    )
    search_clicked = st.button(
        "⌕ Explore Weather",
        use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)


# ==================== SESSION STATE ====================
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None


# ==================== FETCH WEATHER ====================
if search_clicked:
    if not city_name.strip():
        st.warning("Please enter a city name.")

    else:
        api_key = os.getenv("WEATHER_API_KEY")

        if not api_key:
            st.error(
                "API key not found. Add WEATHER_API_KEY to your .env file."
            )

        else:
            try:
                with st.spinner("Fetching current weather..."):
                    response = requests.get(
                        "https://api.openweathermap.org/data/2.5/weather",
                        params={
                            "q": city_name.strip(),
                            "appid": api_key,
                            "units": "metric"
                        },
                        timeout=10
                    )

                try:
                    result = response.json()
                except ValueError:
                    result = {}

                if response.status_code == 200:
                    st.session_state.weather_data = result

                elif response.status_code == 404:
                    st.error("City not found. Check the spelling.")

                elif response.status_code == 401:
                    st.error(
                        "Invalid API key. Check your OpenWeatherMap API key."
                    )

                elif response.status_code == 429:
                    st.error("API request limit reached. Try again later.")

                else:
                    st.error(
                        result.get("message", "Unable to fetch weather data.")
                    )

            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")

            except requests.exceptions.RequestException:
                st.error(
                    "Unable to connect. Check your internet connection."
                )


# ==================== WEATHER DASHBOARD ====================
data = st.session_state.weather_data

if data:
    city = escape(str(data.get("name", city_name)))
    country = escape(str(data.get("sys", {}).get("country", "")))

    main_data = data.get("main", {})
    weather_list = data.get("weather", [])
    wind_data = data.get("wind", {})
    coordinates = data.get("coord", {})

    temp = float(main_data.get("temp", 0))
    feels_like = float(main_data.get("feels_like", temp))
    humidity = int(main_data.get("humidity", 0))
    pressure = int(main_data.get("pressure", 0))
    wind = float(wind_data.get("speed", 0))
    visibility = data.get("visibility")

    description = (
        weather_list[0].get("description", "Unknown")
        if weather_list else "Unknown"
    )

    weather_main = (
        weather_list[0].get("main", "").lower()
        if weather_list else ""
    )

    icon_code = (
        weather_list[0].get("icon", "")
        if weather_list else ""
    )

    icon_map = {
        "01": "☀️",
        "02": "🌤️",
        "03": "⛅",
        "04": "☁️",
        "09": "🌧️",
        "10": "🌦️",
        "11": "⛈️",
        "13": "❄️",
        "50": "🌫️"
    }

    icon = icon_map.get(icon_code[:2], "🌍")

    timezone_offset = int(data.get("timezone", 0))
    local_time = datetime.now(timezone.utc) + timedelta(
        seconds=timezone_offset
    )
    time_text = local_time.strftime("%A, %d %B %Y · %I:%M %p")

    # ---------- CURRENT CONDITIONS ----------
    st.markdown(
        '<div class="section-title">✦ Current Conditions</div>',
        unsafe_allow_html=True
    )

    hero_col, sky_col = st.columns([3, 2], gap="medium")

    with hero_col:
        st.markdown(f"""
        <div class="weather-hero">
            <div class="location-name">
                {city} <span class="country-code">{country}</span>
            </div>
            <div class="local-time">🕒 {time_text} (Local Time)</div>
            <div class="temperature">{round(temp)}°C</div>
            <div class="weather-condition">
                {icon} &nbsp; {escape(description.title())}
            </div>
            <div class="feels-like">Feels like {round(feels_like)}°C</div>
        </div>
        """, unsafe_allow_html=True)

    with sky_col:
        st.markdown(f"""
        <div class="sky-card">
            <div class="sky-caption">THE SKY RIGHT NOW</div>
            <div class="sky-icon">{icon}</div>
            <div class="sky-description">{escape(description.title())}</div>
            <div style="color:#8ca9c6;font-size:13px;margin-top:10px;">
                {city}, {country}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- ATMOSPHERIC INSIGHTS ----------
    st.markdown(
        '<div class="section-title">◈ Atmospheric Insights</div>',
        unsafe_allow_html=True
    )

    def metric_card(column, icon, label, value):
        with column:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="medium")

    metric_card(m1, "💧", "Humidity", f"{humidity}%")
    metric_card(m2, "💨", "Wind Speed", f"{wind:g} m/s")
    metric_card(m3, "◉", "Pressure", f"{pressure} hPa")

    m4, m5, m6 = st.columns(3, gap="medium")

    visibility_text = (
        f"{visibility / 1000:.1f} km"
        if visibility is not None else "N/A"
    )

    metric_card(m4, "👁️", "Visibility", visibility_text)
    metric_card(m5, "🌡️", "Feels Like", f"{round(feels_like)}°C")
    metric_card(
        m6,
        "📍",
        "Coordinates",
        f"{coordinates.get('lat', 0):.2f}, {coordinates.get('lon', 0):.2f}"
    )

    # ==================== DYNAMIC ADVISORIES ====================
    st.markdown(
        '<div class="section-title">🌿 Lifestyle & Smart Weather Advisory</div>',
        unsafe_allow_html=True
    )

    # ---------- OUTDOOR FITNESS ----------
    if weather_main in ["thunderstorm", "rain", "drizzle", "snow"]:
        fitness_title = "Indoor Workout"
        fitness_status = "Weather Caution"
        fitness_advice = (
            "Consider indoor exercise because of current precipitation "
            "or storm conditions."
        )
        fitness_icon = "🏋️"

    elif temp >= 35:
        fitness_title = "Limit Outdoor Exercise"
        fitness_status = "Very Hot Conditions"
        fitness_advice = (
            "Consider exercising during cooler hours, taking breaks, "
            "and drinking water regularly."
        )
        fitness_icon = "🌡️"

    elif temp <= 5:
        fitness_title = "Cold Weather Activity"
        fitness_status = "Keep Warm"
        fitness_advice = (
            "Wear suitable layers and warm up before outdoor activity."
        )
        fitness_icon = "🧥"

    elif wind >= 10:
        fitness_title = "Windy Conditions"
        fitness_status = "Use Caution"
        fitness_advice = (
            "Consider a sheltered exercise location if winds are strong."
        )
        fitness_icon = "💨"

    else:
        fitness_title = "Outdoor Fitness"
        fitness_status = "Check Local Conditions"
        fitness_advice = (
            "Outdoor activity may be suitable. Stay hydrated and "
            "adjust your plans to how you feel."
        )
        fitness_icon = "🏃"

    if humidity >= 80 and temp >= 28:
        fitness_advice += (
            " High humidity may make exercise feel more strenuous."
        )

    # ---------- WHAT TO WEAR ----------
    if temp >= 30:
        wear_title = "Lightweight Clothing"
        wear_advice = (
            "Choose breathable clothing and consider sun protection."
        )
        wear_icon = "👕"

    elif temp >= 20:
        wear_title = "Casual & Comfortable"
        wear_advice = (
            "A T-shirt or light shirt may be comfortable for the day."
        )
        wear_icon = "👔"

    elif temp >= 10:
        wear_title = "Add a Light Layer"
        wear_advice = "Consider a light jacket or an extra layer."
        wear_icon = "🧥"

    else:
        wear_title = "Warm Layers Recommended"
        wear_advice = (
            "Consider warm layers and clothing suitable for cold weather."
        )
        wear_icon = "🧣"

    if weather_main in ["rain", "drizzle", "thunderstorm"]:
        wear_advice += " Consider carrying an umbrella or raincoat."
    elif weather_main == "snow":
        wear_advice += " Consider waterproof footwear and outerwear."

    # ---------- TRAVEL & COMMUTE ----------
    if weather_main == "thunderstorm":
        travel_title = "Travel with Caution"
        travel_status = "Storm Conditions"
        travel_advice = (
            "Check local alerts and travel advisories before leaving. "
            "Consider delaying unnecessary journeys during severe storms."
        )
        travel_icon = "⛈️"

    elif weather_main in ["rain", "drizzle", "snow", "mist", "fog"]:
        travel_title = "Allow Extra Travel Time"
        travel_status = "Weather-Aware Travel"
        travel_advice = (
            "Check road conditions, visibility, and public transit updates "
            "before travelling."
        )
        travel_icon = "🚗"

    elif wind >= 10:
        travel_title = "Check Wind Conditions"
        travel_status = "Strong Winds"
        travel_advice = (
            "Check local travel advisories, particularly for exposed routes."
        )
        travel_icon = "💨"

    elif temp >= 38:
        travel_title = "Plan Around the Heat"
        travel_status = "Hot Conditions"
        travel_advice = (
            "Carry drinking water and consider limiting prolonged outdoor "
            "waiting during the hottest part of the day."
        )
        travel_icon = "☀️"

    else:
        travel_title = "Plan Your Journey"
        travel_status = "Check Local Traffic"
        travel_advice = (
            "Check live traffic and transit information before travelling. "
            "Weather alone cannot predict road conditions."
        )
        travel_icon = "🚲"

    # ---------- ADVISORY CARD FUNCTION ----------
    def advisory_card(column, icon, title, status, advice):
        with column:
            st.markdown(f"""
            <div class="advisory-card">
                <div class="advisory-heading">
                    <span class="advisory-icon">{icon}</span>
                    <div>
                        <div class="advisory-title">{escape(title)}</div>
                        <div class="advisory-status">{escape(status)}</div>
                    </div>
                </div>
                <div class="advisory-description">{escape(advice)}</div>
            </div>
            """, unsafe_allow_html=True)

    fitness_col, wear_col, travel_col = st.columns(3, gap="medium")

    advisory_card(
        fitness_col,
        fitness_icon,
        fitness_title,
        fitness_status,
        fitness_advice
    )

    advisory_card(
        wear_col,
        wear_icon,
        wear_title,
        "Based on current temperature",
        wear_advice
    )

    advisory_card(
        travel_col,
        travel_icon,
        travel_title,
        travel_status,
        travel_advice
    )

else:
    st.markdown("""
    <div class="weather-hero" style="text-align:center;padding:45px 20px;min-height:0;">
        <div style="font-size:60px;">🌍</div>
        <div style="font-size:25px;font-weight:800;margin:15px 0;color:white;">
            Your next weather discovery awaits.
        </div>
        <div style="color:#a7bbd1;line-height:1.8;">
            Search for a city above to discover its current weather,<br>
            atmospheric insights and personalized weather advice.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <div style="color:#dceafa;font-size:15px;font-weight:750;margin-bottom:7px;">
        ✦ ClimaSense
    </div>
    Weather data powered by OpenWeatherMap API
    &nbsp;·&nbsp; Built with Streamlit
    <br><br>
    Weather recommendations provide general guidance,
    not live traffic information or official safety alerts.
</div>
""", unsafe_allow_html=True)

