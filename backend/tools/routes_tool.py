import os
import requests

def get_transit_options(origin: str, destination: str, mode: str = "TRANSIT") -> dict:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.legs,routes.description"
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": mode,
        "computeAlternativeRoutes": False,
        "languageCode": "en"
    }
    if mode == "TRANSIT":
        body["transitPreferences"] = {"routingPreference": "LESS_WALKING"}
    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()
        routes = data.get("routes", [])
        if not routes:
            return {"mode": mode, "duration": "Unknown", "distance": "Unknown", "instructions": "Route not available", "estimated_cost": "N/A"}
        route = routes[0]
        duration_seconds = int(route.get("duration", "0s").replace("s", ""))
        duration_minutes = round(duration_seconds / 60)
        distance_meters = route.get("distanceMeters", 0)
        distance_km = round(distance_meters / 1000, 1)
        legs = route.get("legs", [])
        steps_summary = []
        for leg in legs:
            for step in leg.get("steps", []):
                travel_mode = step.get("travelMode", "")
                if travel_mode == "TRANSIT":
                    transit_details = step.get("transitDetails", {})
                    line = transit_details.get("transitLine", {}).get("name", "Transit")
                    steps_summary.append(f"Take {line}")
                elif travel_mode == "WALK":
                    walk_duration = int(step.get("staticDuration", "0s").replace("s", ""))
                    steps_summary.append(f"Walk {round(walk_duration/60)} min")
        mode_label = {"TRANSIT": "Public Transport", "WALK": "Walking", "DRIVE": "Drive/Cab", "BICYCLE": "Cycling"}.get(mode, mode)
        return {
            "mode": mode_label,
            "duration": f"{duration_minutes} min",
            "distance": f"{distance_km} km",
            "instructions": " -> ".join(steps_summary) if steps_summary else f"{mode_label} route",
            "estimated_cost": "Free" if mode in ["WALK", "BICYCLE"] else "Varies"
        }
    except Exception as e:
        print(f"Routes API error: {e}")
        return {"mode": mode, "duration": "~15 min", "distance": "Unknown", "instructions": "Check Google Maps for directions", "estimated_cost": "N/A"}
