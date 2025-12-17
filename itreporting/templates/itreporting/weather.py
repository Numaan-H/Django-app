import requests

city_name = 'york'
api_key = '2474636061ab426f55d6f07da1b3d43f'
url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print('Weather is',data['weather'][0]['description'])
    print('Current temperature is',data['main']['temp'])
    print('Feels like',data['main']['feels_like'])
    print('Humidity:',data['main']['humidity'])
else:
    print("Error loading weather")