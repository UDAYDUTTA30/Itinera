from datetime import datetime

def create_calendar_events(itinerary: dict) -> dict:
    events_created = []
    stops = itinerary.get("stops", [])
    date_str = itinerary.get("date", datetime.now().strftime("%Y-%m-%d"))
    for stop in stops:
        event = {
            "summary": f"Itinera: {stop.get('name', 'Visit')}",
            "location": stop.get("address", ""),
            "description": (
                f"Planned by Itinera\n"
                f"Rating: {stop.get('rating', 'N/A')}\n"
                f"Estimated cost: {stop.get('estimated_cost', 'N/A')}\n"
                f"Maps: {stop.get('maps_link', '')}\n"
                f"Notes: {stop.get('notes', '')}"
            ),
            "start_time": f"{date_str}T{stop.get('time', '12:00')}:00",
            "reminders": [{"method": "popup", "minutes": 30}],
            "status": "confirmed"
        }
        events_created.append(event)
    return {
        "success": True,
        "events_created": len(events_created),
        "events": events_created,
        "message": f"Successfully created {len(events_created)} calendar events for your plan!"
    }
