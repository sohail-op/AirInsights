from flask import Blueprint, request, jsonify
from flight_scraper import get_scraped_flights
from dateutil.parser import isoparse
from datetime import datetime
import re

filter_bp = Blueprint('filter', __name__)

def validate_country_code(country):
    """Validate and normalize country code/name"""
    if not country:
        return None
    
    country_mappings = {
        'australia': 'Australia',
        'au': 'Australia',
        'usa': 'United States',
        'us': 'United States',
        'united states': 'United States',
        'united states of america': 'United States',
        'uk': 'United Kingdom',
        'united kingdom': 'United Kingdom',
        'great britain': 'United Kingdom',
        'canada': 'Canada',
        'ca': 'Canada',
        'germany': 'Germany',
        'de': 'Germany',
        'france': 'France',
        'fr': 'France',
        'japan': 'Japan',
        'jp': 'Japan',
        'china': 'China',
        'cn': 'China',
        'india': 'India',
        'in': 'India',
        'brazil': 'Brazil',
        'br': 'Brazil',
        'russia': 'Russia',
        'ru': 'Russia',
        'south africa': 'South Africa',
        'za': 'South Africa',
        'new zealand': 'New Zealand',
        'nz': 'New Zealand'
    }
    
    country_lower = country.lower().strip()
    return country_mappings.get(country_lower, country)

def validate_date_range(start, end):
    """Validate date range parameters"""
    try:
        if start:
            start_dt = isoparse(start)
        else:
            start_dt = None
            
        if end:
            end_dt = isoparse(end)
        else:
            end_dt = None
            
        if start_dt and end_dt and start_dt > end_dt:
            return None, "Start date must be before end date"
            
        return (start_dt, end_dt), None
    except ValueError as e:
        return None, f"Invalid date format: {str(e)}"

@filter_bp.route('/flights/filter', methods=['GET'])
def filter_flights():
    """
    Filter flights based on various criteria using real-time data from FlightRadar24 & OpenSky APIs:
    
    Query Parameters:
    - country: Country name or code (e.g., 'Australia', 'AU', 'USA', 'US')
    - start: Start date/time (ISO 8601 format) - Note: Limited functionality with real-time data
    - end: End date/time (ISO 8601 format) - Note: Limited functionality with real-time data
    - on_ground: Filter by ground status ('true'/'false')
    - min_speed: Minimum velocity in km/h
    - max_speed: Maximum velocity in km/h
    - limit: Maximum number of results (default: 100, max: 1000)
    """
    try:

        country = request.args.get('country', '').strip()
        start = request.args.get('start', '').strip()
        end = request.args.get('end', '').strip()
        on_ground = request.args.get('on_ground', '').strip()
        min_speed = request.args.get('min_speed', '').strip()
        max_speed = request.args.get('max_speed', '').strip()
        limit = request.args.get('limit', '100').strip()
        

        errors = []
        

        normalized_country = validate_country_code(country) if country else None
        

        date_range, date_error = validate_date_range(start, end)
        if date_error:
            errors.append(date_error)
        

        if on_ground and on_ground.lower() not in ['true', 'false']:
            errors.append("on_ground parameter must be 'true' or 'false'")
        

        min_speed_val = None
        max_speed_val = None
        try:
            min_speed_val = float(min_speed) if min_speed else None
            max_speed_val = float(max_speed) if max_speed else None
            if min_speed_val is not None and min_speed_val < 0:
                errors.append("min_speed must be non-negative")
            if max_speed_val is not None and max_speed_val < 0:
                errors.append("max_speed must be non-negative")
            if min_speed_val is not None and max_speed_val is not None and min_speed_val > max_speed_val:
                errors.append("min_speed must be less than or equal to max_speed")
        except ValueError:
            errors.append("Speed parameters must be valid numbers")
        

        limit_val = 100
        try:
            limit_val = int(limit)
            if limit_val < 1 or limit_val > 1000:
                errors.append("limit must be between 1 and 1000")
        except ValueError:
            errors.append("limit must be a valid integer")
        
        if errors:
            return jsonify({"error": "Validation errors", "details": errors}), 400
        

        on_ground_val = None
        if on_ground:
            on_ground_val = on_ground.lower() == 'true'
        

        flights = get_scraped_flights()
        filtered = []
        
        for flight in flights:
    
            
    
            if normalized_country:
                flight_country = flight.get("origin_country", "")
                if not flight_country or flight_country.lower() != normalized_country.lower():
                    continue
            
    
            if on_ground_val is not None and flight.get("on_ground") != on_ground_val:
                continue
            
    
            velocity = flight.get("velocity_kmh", 0)
            if min_speed_val is not None and velocity < min_speed_val:
                continue
            if max_speed_val is not None and velocity > max_speed_val:
                continue
        
            
            filtered.append(flight)
            
    
            if len(filtered) >= limit_val:
                break
        

        response = {
            "count": len(filtered),
            "total_available": len(flights),
            "filters_applied": {
                "country": normalized_country if country else None,
                "on_ground": on_ground_val if on_ground else None,
                "min_speed": min_speed_val if min_speed else None,
                "max_speed": max_speed_val if max_speed else None,
                "start": start if start else None,
                "end": end if end else None,
                "limit": limit_val
            },
            "flights": filtered,
            "timestamp": datetime.utcnow().isoformat(),
            "data_source": "FlightRadar24 & OpenSky APIs",
            "note": "Real-time flight data from legitimate aviation APIs. Time filtering is limited with current data sources."
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
