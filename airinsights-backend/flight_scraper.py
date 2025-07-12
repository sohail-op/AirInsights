import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class FlightDataFetcher:
    """
    Real-time flight data fetcher using legitimate APIs
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_flightradar_data(self) -> List[Dict]:
        """
        Fetch real flight data from FlightRadar24 public API
        """
        try:
    
            url = "https://data-live.flightradar24.com/zones/fcgi/feed.js"
            params = {
                'bounds': '-44,-10,112,154',
                'faa': '1',
                'mlat': '1',
                'flarm': '1',
                'adsb': '1',
                'gnd': '1',
                'air': '1',
                'vehicles': '1',
                'estimated': '1',
                'maxage': '7200',
                'gliders': '1',
                'stats': '1'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            flights = []
            
    
            aircraft_data = data.get('aircraft', {})
            
    
            if isinstance(aircraft_data, dict):
                for icao24, flight_data in aircraft_data.items():
                    if isinstance(flight_data, list) and len(flight_data) >= 14:
                        try:
                            flight = {
                                "icao24": icao24,
                                "callsign": flight_data[16] if len(flight_data) > 16 else None,
                                "latitude": flight_data[1],
                                "longitude": flight_data[2],
                                "altitude": flight_data[4],
                                "velocity_kmh": round(flight_data[5] * 1.852, 2) if flight_data[5] else 0,
                                "vertical_rate": flight_data[6],
                                "on_ground": flight_data[8] == 1,
                                "origin_country": "Australia",
                                "destination_country": "Australia",
                                "origin_airport": flight_data[11] if len(flight_data) > 11 else None,
                                "destination_airport": flight_data[12] if len(flight_data) > 12 else None,
                                "timestamp": datetime.utcnow().isoformat()
                            }
                            flights.append(flight)
                        except (IndexError, TypeError):
                            continue
            elif isinstance(aircraft_data, list):
        
                for flight_data in aircraft_data:
                    if isinstance(flight_data, list) and len(flight_data) >= 14:
                        try:
                            flight = {
                                "icao24": flight_data[0] if len(flight_data) > 0 else None,
                                "callsign": flight_data[16] if len(flight_data) > 16 else None,
                                "latitude": flight_data[1],
                                "longitude": flight_data[2],
                                "altitude": flight_data[4],
                                "velocity_kmh": round(flight_data[5] * 1.852, 2) if flight_data[5] else 0,
                                "vertical_rate": flight_data[6],
                                "on_ground": flight_data[8] == 1,
                                "origin_country": "Australia",
                                "destination_country": "Australia",
                                "origin_airport": flight_data[11] if len(flight_data) > 11 else None,
                                "destination_airport": flight_data[12] if len(flight_data) > 12 else None,
                                "timestamp": datetime.utcnow().isoformat()
                            }
                            flights.append(flight)
                        except (IndexError, TypeError):
                            continue
            
            return flights
            
        except Exception as e:
            print(f"Error fetching FlightRadar24 data: {e}")
            return []
    
    def get_opensky_data(self) -> List[Dict]:
        """
        Fetch real flight data from OpenSky Network API
        """
        try:
    
            url = "https://opensky-network.org/api/states/all"
            params = {
                'lamin': -44.0,
                'lamax': -10.0,
                'lomin': 112.0,
                'lomax': 154.0
            }
            
    
            auth = None
            username = "your_opensky_username"
            password = "your_opensky_password"
            
            if username != "your_opensky_username" and password != "your_opensky_password":
                auth = (username, password)
            
            response = self.session.get(url, params=params, auth=auth, timeout=10)
            
    
            if response.status_code == 429:
                print("OpenSky API rate limited, skipping...")
                return []
            
            response.raise_for_status()
            
            data = response.json()
            flights = []
            
            for state in data.get('states', []):
                if len(state) >= 17:
                    try:
                        flight = {
                            "icao24": state[0],
                            "callsign": state[1].strip() if state[1] else None,
                            "origin_country": state[2],
                            "timestamp": state[3],
                            "longitude": state[5],
                            "latitude": state[6],
                            "altitude": state[7],
                            "velocity_kmh": state[9] * 3.6 if state[9] else 0,
                            "vertical_rate": state[11],
                            "on_ground": state[8],
                            "origin_airport": None,
                            "destination_airport": None,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        flights.append(flight)
                    except (IndexError, TypeError):
                        continue
            
            return flights
            
        except Exception as e:
            print(f"Error fetching OpenSky data: {e}")
            return []
    
    def get_all_real_flight_data(self) -> List[Dict]:
        """
        Combine real data from legitimate sources only
        """
        all_flights = []
        

        sources = [
            self.get_flightradar_data,
            self.get_opensky_data
        ]
        
        for source_func in sources:
            try:
                flights = source_func()
                all_flights.extend(flights)
                time.sleep(1)
            except Exception as e:
                print(f"Error with data source {source_func.__name__}: {e}")
                continue
        

        unique_flights = {}
        for flight in all_flights:
            icao24 = flight.get("icao24")
            if icao24 and icao24 not in unique_flights:
                unique_flights[icao24] = flight
        
        return list(unique_flights.values())
    
    def get_flights_by_region(self, bounds: tuple = (-44.0, -10.0, 112.0, 154.0)) -> List[Dict]:
        """
        Get real flights within specific geographic bounds
        """
        all_flights = self.get_all_real_flight_data()
        min_lat, max_lat, min_lon, max_lon = bounds
        
        filtered_flights = []
        for flight in all_flights:
            lat = flight.get("latitude")
            lon = flight.get("longitude")
            
            if lat is not None and lon is not None:
                if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                    filtered_flights.append(flight)
        
        return filtered_flights
flight_fetcher = FlightDataFetcher()

def get_scraped_flights(bounds: tuple = (-44.0, -10.0, 112.0, 154.0)) -> List[Dict]:
    """
    Main function to get real flight data
    """
    return flight_fetcher.get_flights_by_region(bounds) 