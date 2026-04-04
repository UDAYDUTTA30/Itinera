import os
import requests

def find_spots(location: str, activity_type: str, vibe: str = "", budget_level: int = 2, limit: int = 5) -> list:
    """Find real spots using Google Places API (New)."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if not api_key:
        print("ERROR: GOOGLE_MAPS_API_KEY not set")
        return [{"error": "GOOGLE_MAPS_API_KEY environment variable not set"}]
    
    url = "https://places.googleapis.com/v1/places:searchText"
    query = f"{vibe} {activity_type} in {location}".strip()
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.priceLevel,places.googleMapsUri,places.currentOpeningHours,places.editorialSummary,places.id"
    }
    
    body = {"textQuery": query, "maxResultCount": limit, "languageCode": "en"}
    
    if budget_level == 1:
        body["priceLevels"] = ["PRICE_LEVEL_INEXPENSIVE"]
    elif budget_level == 2:
        body["priceLevels"] = ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE"]
    elif budget_level == 3:
        body["priceLevels"] = ["PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE"]
    elif budget_level == 4:
        body["priceLevels"] = ["PRICE_LEVEL_VERY_EXPENSIVE"]

    print(f"DEBUG: Calling Places API with query: {query}")
    print(f"DEBUG: Using API key ending in: ...{api_key[-6:]}")

    try:
        response = requests.post(url, json=body, headers=headers)
        
        print(f"DEBUG: Places API status code: {response.status_code}")
        
        if response.status_code == 403:
            error_body = response.json()
            error_msg = error_body.get("error", {}).get("message", "Unknown 403 error")
            print(f"ERROR 403: {error_msg}")
            return [{"error": f"Places API Error 403: {error_msg}. Check GOOGLE_MAPS_API_KEY permissions."}]
        
        if response.status_code == 400:
            error_body = response.json()
            error_msg = error_body.get("error", {}).get("message", "Unknown 400 error")
            print(f"ERROR 400: {error_msg}")
            return [{"error": f"Places API Error 400: {error_msg}"}]
        
        response.raise_for_status()
        data = response.json()
        
        places = data.get("places", [])
        print(f"DEBUG: Places API returned {len(places)} results")
        
        if not places:
            print(f"DEBUG: No places found for query: {query}")
            return []
        
        spots = []
        for place in places:
            spot = {
                "name": place.get("displayName", {}).get("text", "Unknown"),
                "address": place.get("formattedAddress", ""),
                "rating": place.get("rating", None),
                "maps_link": place.get("googleMapsUri", ""),
                "summary": place.get("editorialSummary", {}).get("text", ""),
                "price_level": place.get("priceLevel", ""),
                "place_id": place.get("id", ""),
                "is_open": place.get("currentOpeningHours", {}).get("openNow", None),
            }
            spots.append(spot)
        
        spots.sort(key=lambda x: x.get("rating") or 0, reverse=True)
        print(f"DEBUG: Returning {len(spots)} spots")
        return spots

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Places API request failed: {str(e)}")
        return [{"error": f"Places API request failed: {str(e)}"}]
    except Exception as e:
        print(f"ERROR: Unexpected error in find_spots: {str(e)}")
        return [{"error": f"Unexpected error: {str(e)}"}]
