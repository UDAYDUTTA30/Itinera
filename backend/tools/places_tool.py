import os
import requests

def find_spots(location: str, activity_type: str, vibe: str = "", budget_level: int = 2, limit: int = 5) -> list:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
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
    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        data = response.json()
        spots = []
        for place in data.get("places", []):
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
        return spots
    except Exception as e:
        print(f"Places API error: {e}")
        return []
