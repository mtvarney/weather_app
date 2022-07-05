import requests

API_KEY = ""
weather_params = {
    "units": "imperial",
}


# Class to manage getting current weather data
class Weather:
    def __init__(self, zip_code):
        # Convert zip code to latitude/longitude
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={API_KEY}"
        geocoding_response = requests.get(url=geocoding_url)

        self.name = geocoding_response.json()["name"]
        self.lat = geocoding_response.json()["lat"]
        self.lon = geocoding_response.json()["lon"]
        # Get weather data
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={API_KEY}"
        weather_response = requests.get(url=weather_url, params=weather_params)

        self.current_temp = weather_response.json()["main"]["temp"]
        self.weather_code = str(weather_response.json()["weather"][0]["id"])
        self.weather_description = weather_response.json()["weather"][0]["description"].title()
        self.image = self.update_weather_status(self.weather_code)

    # Determine weather picture based on status code
    def update_weather_status(self, code):
        if code[0] == "2":
            self.image = "images/thunderstorm.png"
        elif code[0] == "3":
            self.image = "images/shower_rain.png"
        elif code[0] == "5":
            self.image = "images/rain.png"
        elif code[0] == "6":
            self.image = "images/snow.png"
        elif code[0] == "7":
            self.image = "images/mist.png"
        elif code == "800":
            self.image = "images/clear_sky.png"
        elif code == "801":
            self.image = "images/few_clouds.png"
        elif code == "802":
            self.image = "images/scattered_clouds.png"
        elif code == "803" or code == "804":
            self.image = "images/broken_clouds.png"

        return self.image
