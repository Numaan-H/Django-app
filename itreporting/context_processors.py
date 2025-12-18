import requests

def weather_context(request):
    city_name = request.session.get("weather_city", "York")
    api_key = "2474636061ab426f55d6f07da1b3d43f"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city_name}&appid={api_key}&units=metric"
    )

    weather = None

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": city_name,
                "description": data["weather"][0]["description"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
            }
    except requests.RequestException:
        pass

    return {"weather": weather}
