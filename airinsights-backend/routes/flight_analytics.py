
from flask import Blueprint, jsonify
from aviation import get_flight_data
from collections import Counter
from datetime import datetime
from utils import clean_airport_name

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/flights/analytics', methods=['GET'])
def flight_analytics():
    try:
    
        flights = get_flight_data(limit=100)
        
    
        if not flights:
            return jsonify({
                "error": "No real-time flight data available from AviationStack API",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 503
        
        origin_countries = []
        dest_countries = []
        origin_airports = []
        dest_airports = []
        scheduled = 0
        active = 0

        for flight in flights:
        
            dep_airport = flight.get("departure_airport", "Unknown")
            arr_airport = flight.get("arrival_airport", "Unknown")
            
            origin_airports.append(clean_airport_name(dep_airport))
            dest_airports.append(clean_airport_name(arr_airport))
            
        
            origin_country = dep_airport.split()[-1] if dep_airport != "Unknown" else "Unknown"
            dest_country = arr_airport.split()[-1] if arr_airport != "Unknown" else "Unknown"
            
            origin_countries.append(origin_country)
            dest_countries.append(dest_country)
            
        
            status = flight.get("status", "scheduled")
            if status == "active":
                active += 1
            else:
                scheduled += 1

        response = {
            "top_origin_airports": Counter(origin_airports).most_common(5),
            "top_destination_airports": Counter(dest_airports).most_common(5),
            "top_origin_countries": Counter(origin_countries).most_common(5),
            "top_destination_countries": Counter(dest_countries).most_common(5),
            "status_distribution": {
                "active": active,
                "scheduled": scheduled
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data_source": "AviationStack API"
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/flights/trends', methods=['GET'])
def trend_analytics():
    """
    Trend Analytics endpoint providing real-time data from AviationStack API:
    - Popular routes analysis
    - Price trends (based on flight frequency and demand)
    - High-demand locations
    """
    try:
    
        flights = get_flight_data(limit=100)
        
    
        if not flights:
            return jsonify({
                "error": "No real-time flight data available from AviationStack API",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 503
        

        
    
        routes = []
        airlines = []
        departure_airports = []
        arrival_airports = []
        
        for flight in flights:
            if flight.get('departure_airport') and flight.get('arrival_airport'):
            
                dep_airport = flight['departure_airport']
                arr_airport = flight['arrival_airport']
                
            
                dep_short = clean_airport_name(dep_airport)
                arr_short = clean_airport_name(arr_airport)
                route = f"{dep_short} → {arr_short}"
                
                routes.append(route)
                airlines.append(flight.get('airline', 'Unknown'))
                departure_airports.append(dep_airport) 
                arrival_airports.append(arr_airport)   
        
    
        route_counts = Counter(routes)
        popular_routes = [
            {
                "route": route,
                "frequency": count,
                "demand_level": "High" if count >= 5 else "Medium" if count >= 3 else "Low"
            }
            for route, count in route_counts.most_common(10)
        ]
        
    
        departure_counts = Counter(departure_airports)
        arrival_counts = Counter(arrival_airports)
        
    
        all_airports = departure_counts + arrival_counts
        

        
        high_demand_locations = [
            {
                "airport": clean_airport_name(airport),
                "total_flights": count,
                "departures": departure_counts.get(airport, 0),
                "arrivals": arrival_counts.get(airport, 0),
                "demand_category": "Very High" if count >= 15 else "High" if count >= 10 else "Medium" if count >= 5 else "Low"
            }
            for airport, count in all_airports.most_common(15)
        ]
        
    
        airline_counts = Counter(airlines)
        competitive_routes = []
        
        for route, count in route_counts.items():
            if count >= 3: 
                route_airlines = [flight.get('airline', 'Unknown') for flight in flights 
                                if f"{flight.get('departure_airport')} → {flight.get('arrival_airport')}" == route]
                unique_airlines = len(set(route_airlines))
                
                competitive_routes.append({
                    "route": route,
                    "flight_frequency": count,
                    "airline_competition": unique_airlines,
                    "price_pressure": "High" if unique_airlines >= 3 else "Medium" if unique_airlines >= 2 else "Low"
                })
        
    
        competitive_routes.sort(key=lambda x: x['airline_competition'], reverse=True)
        
    
        top_airlines = [
            {
                "airline": airline,
                "flight_count": count,
                "market_share": round((count / len(flights)) * 100, 2)
            }
            for airline, count in airline_counts.most_common(10)
        ]
        
    
        time_distribution = {}
        for flight in flights:
            if flight.get('departure_time'):
                try:
                
                    if isinstance(flight['departure_time'], str):
                    
                        departure_dt = datetime.fromisoformat(flight['departure_time'].replace('Z', '+00:00'))
                    else:
                    
                        departure_dt = datetime.fromtimestamp(flight['departure_time'] / 1000)
                    
                    departure_hour = departure_dt.hour
                    time_slot = f"{departure_hour:02d}:00-{(departure_hour+1)%24:02d}:00"
                    time_distribution[time_slot] = time_distribution.get(time_slot, 0) + 1
                except Exception as e:
                    print(f"Error processing departure time: {e}")
                    continue
        
    
        peak_hours = sorted(time_distribution.items(), key=lambda x: int(x[0][:2]))
        
        response = {
            "popular_routes": {
                "top_routes": popular_routes,
                "total_unique_routes": len(route_counts)
            },
            "high_demand_locations": {
                "airports": high_demand_locations,
                "total_airports": len(all_airports)
            },
            "price_trends": {
                "competitive_routes": competitive_routes[:10],
                "top_airlines": top_airlines,
                "market_insights": {
                    "total_flights_analyzed": len(flights),
                    "average_competition_per_route": round(sum(r['airline_competition'] for r in competitive_routes) / len(competitive_routes), 2) if competitive_routes else 0
                }
            },
            "time_analysis": {
                "peak_departure_hours": [{"time_slot": slot, "flight_count": count} for slot, count in peak_hours],
                "total_time_slots_analyzed": len(time_distribution)
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data_source": "AviationStack API"
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
