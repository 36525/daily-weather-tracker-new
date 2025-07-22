import requests
import csv
from datetime import datetime

API_KEY = '9d87b35ef81c86659aedec4d1b549965'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
CSV_FILE = 'daily_weather.csv'

# Vietovių sąrašas su pavadinimais, koordinatėmis ir aukščiu
locations = [
    ("Vilnius", "54.6872", "25.2797", 112),
    ("Stambulas", "41.0082", "28.9784", 40),
    ("Islamabadas", "33.6844", "73.0479", 540),
    ("Skardu", "35.3350", "75.5407", 2230),
    ("Askoli / Korfong", "35.6819", "75.8341", 3000),
    ("Mongron", "35.7480", "75.8690", 3140),
    ("Paju", "35.7890", "75.8942", 3666),
    ("Khoburse", "35.8190", "75.9245", 3833),
    ("Goro 1", "35.8255", "76.0051", 4000),
    ("Concordia", "35.8687", "76.5133", 4691),
    ("Broad Peak BC", "35.8126", "76.5167", 5177),
    ("K2 BC", "35.7575", "76.5133", 4998),
    ("Ali Camp", "35.6981", "76.5183", 5000),
    ("Gondogoro La", "35.6500", "76.5417", 5585),
    ("Khuspang", "35.6164", "76.5458", 4600),
    ("Saicho", "35.5840", "76.4666", 3500),
    ("Hushe", "35.4306", "76.3331", 3000),
    ("K2 Summit", "35.8808", "76.5133", 8611),
    # Papildomos žymios vietos
    ("Everest Base Camp", "28.0026", "86.8528", 5364),
    ("Everest Summit", "27.9881", "86.9250", 8848),
    ("Dead Sea (lowest point)", "31.5590", "35.4732", -430),
    ("Kilimanjaro Summit", "-3.0758", "37.3533", 5895),
    ("Aconcagua Summit", "-32.6532", "-70.0109", 6961),
]

# CSV stulpeliai
headers = [
    'date', 'city', 'altitude_m', 'temp', 'feels_like', 'humidity',
    'wind_speed', 'wind_deg', 'pressure', 'clouds_all', 'visibility',
    'description', 'rain_mm', 'showers_mm', 'snowfall_cm'
]

# Vienos vietovės orų duomenų surinkimas
def fetch_weather(city, lat, lon, altitude):
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    return {
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'city': city,
        'altitude_m': altitude,
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'wind_deg': data['wind'].get('deg', ''),
        'pressure': data['main']['pressure'],
        'clouds_all': data['clouds']['all'],
        'visibility': data.get('visibility', ''),
        'description': data['weather'][0]['description'],
        'rain_mm': data.get('rain', {}).get('1h', 0),
        'showers_mm': data.get('rain', {}).get('3h', 0),
        'snowfall_cm': data.get('snow', {}).get('1h', 0)
    }

# Pagrindinė funkcija
def main():
    all_data = []
    for city, lat, lon, altitude in locations:
        try:
            weather = fetch_weather(city, lat, lon, altitude)
            all_data.append(weather)
            print(f"✅ {city} – duomenys gauti")
        except Exception as e:
            print(f"❌ Klaida su {city}: {e}")

    file_exists = False
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerows(all_data)

if __name__ == "__main__":
    main()
