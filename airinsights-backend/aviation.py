import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
BASE_URL = "http://api.aviationstack.com/v1/flights"

def get_flight_data(limit=50):
    if not API_KEY or API_KEY == "your_api_key_here":
        raise Exception("AviationStack API key is missing. Please set it in your .env file.")
    params = {
        "access_key": API_KEY,
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from AviationStack: {response.status_code} {response.text}")
    flights = response.json().get("data", [])
    return [
        {
            "airline": f.get("airline", {}).get("name"),
            "flight_number": f.get("flight", {}).get("iata"),
            "departure_airport": f.get("departure", {}).get("airport"),
            "arrival_airport": f.get("arrival", {}).get("airport"),
            "departure_country": f.get("departure", {}).get("country"),
            "arrival_country": f.get("arrival", {}).get("country"),
            "departure_time": f.get("departure", {}).get("scheduled"),
            "arrival_time": f.get("arrival", {}).get("scheduled"),
            "status": f.get("flight_status")
        }
        for f in flights if f.get("departure") and f.get("arrival")
    ]
