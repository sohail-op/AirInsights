from flask import Flask, jsonify, request
from flask_cors import CORS
from aviation import get_flight_data
from flight_scraper import get_scraped_flights
from gemini import analyze_with_gemini
from routes.filtered_flights import filter_bp
from routes.flight_analytics import analytics_bp
from datetime import datetime
from utils import clean_airport_name


app = Flask(__name__)
CORS(app)

app.register_blueprint(filter_bp)
app.register_blueprint(analytics_bp)

@app.route("/flights", methods=["GET"])
def fetch_aviationstack():
    try:
        raw_data = get_flight_data(limit=50)
        if not raw_data:
            return jsonify({"error": "No flight data available"}), 500
        

        return jsonify(raw_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/scraped", methods=["GET"])
def fetch_real_time_flights():
    try:

        traffic = get_scraped_flights()
        if not traffic:
            return jsonify({
                "error": "No real-time flight data available from FlightRadar24 or OpenSky APIs",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 503
        return jsonify(traffic)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/insights", methods=["POST"])
def generate_insights():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Missing data"}), 400
        insights = analyze_with_gemini(json_data)
        return jsonify({"insights": insights})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/flights/dashboard", methods=["GET"])
def get_dashboard_data():
    try:

        try:
            aviation_flights = get_flight_data(limit=100)
        except Exception as api_error:
            return jsonify({
                "error": f"Failed to fetch data from AviationStack API: {str(api_error)}",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 503
        

        if not aviation_flights or not isinstance(aviation_flights, list):
            return jsonify({
                "error": "No real-time flight data available from AviationStack API",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 503
        

        origin_airports = []
        dest_airports = []
        scheduled = 0
        active = 0



        for flight in aviation_flights:
    
            dep_airport = flight.get("departure_airport") or "Unknown"
            arr_airport = flight.get("arrival_airport") or "Unknown"
            
            origin_airports.append(clean_airport_name(dep_airport))
            dest_airports.append(clean_airport_name(arr_airport))
            
    
            status = flight.get("status") or "scheduled"
            if status == "active":
                active += 1
            else:
                scheduled += 1

        from collections import Counter
        
        flight_overview = {
            "airports": {
                "origin": [{"name": airport, "value": count} for airport, count in Counter(origin_airports).most_common(5)] if origin_airports else [],
                "destination": [{"name": airport, "value": count} for airport, count in Counter(dest_airports).most_common(5)] if dest_airports else []
            },
            "status": [
                {"name": "Active", "value": active},
                {"name": "Scheduled", "value": scheduled}
            ]
        }
        

        routes = []
        airlines = []
        departure_airports = []
        arrival_airports = []
        
        for flight in aviation_flights:
            dep_airport = flight.get('departure_airport')
            arr_airport = flight.get('arrival_airport')
            
            if dep_airport and arr_airport:
        
                dep_short = clean_airport_name(dep_airport)
                arr_short = clean_airport_name(arr_airport)
                route = f"{dep_short} → {arr_short}"
                
                routes.append(route)
                airlines.append(flight.get('airline') or 'Unknown')
                departure_airports.append(dep_airport)
                arrival_airports.append(arr_airport)  
        
        route_counts = Counter(routes)
        departure_counts = Counter(departure_airports)
        arrival_counts = Counter(arrival_airports)
        airline_counts = Counter(airlines)
        
        all_airports = departure_counts + arrival_counts
        

        time_distribution = {}
        for flight in aviation_flights:
            if flight.get('departure_time'):
                try:
            
                    if isinstance(flight['departure_time'], str):
                
                        departure_dt = datetime.fromisoformat(flight['departure_time'].replace('Z', '+00:00'))
                    else:
                
                        departure_dt = datetime.fromtimestamp(flight['departure_time'] / 1000)
                    
                    departure_hour = departure_dt.hour
                    time_slot = f"{departure_hour:02d}:00-{(departure_hour+1):02d}:00"
                    time_distribution[time_slot] = time_distribution.get(time_slot, 0) + 1
                except Exception as e:
                    print(f"Error processing departure time: {e}")
                    continue
        

        peak_hours = sorted(time_distribution.items(), key=lambda x: x[1], reverse=True)[:8]
        
        trend_analysis = {
            "routes": {
                "popular": [
                    {
                        "name": route,
                        "frequency": count,
                        "demand": "High" if count >= 5 else "Medium" if count >= 3 else "Low"
                    }
                    for route, count in route_counts.most_common(10)
                ] if routes else []
            },
            "airports": {
                "high_demand": [
                    {
                        "name": airport,
                        "total_flights": count,
                        "departures": departure_counts.get(airport, 0),
                        "arrivals": arrival_counts.get(airport, 0)
                    }
                    for airport, count in all_airports.most_common(10)
                ] if departure_airports or arrival_airports else []
            },
            "airlines": {
                "top_performers": [
                    {
                        "name": airline,
                        "market_share": round((count / len(aviation_flights)) * 100, 2)
                    }
                    for airline, count in airline_counts.most_common(10)
                ] if airlines else []
            },
            "time_analysis": {
                "peak_hours": [{"time": slot, "flights": count} for slot, count in peak_hours] if peak_hours else []
            }
        }
        
        dashboard_summary = {
            "total_active_flights": len(aviation_flights),
            "unique_routes": len(route_counts),
            "active_airports": len(all_airports),
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "data_source": "AviationStack API"
        }
        
        return jsonify({
            "flight_overview": flight_overview,
            "trend_analysis": trend_analysis,
            "dashboard_summary": dashboard_summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
