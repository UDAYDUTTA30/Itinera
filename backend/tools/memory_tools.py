import json
import requests

TOOLBOX_URL = "https://itinera-toolbox-662889849418.us-central1.run.app"

def save_plan(user_id: str, query: str, itinerary: dict, scores: dict) -> bool:
    try:
        response = requests.post(f"{TOOLBOX_URL}/tools/save-plan/invoke", json={
            "user_id": user_id,
            "query": query,
            "itinerary": json.dumps(itinerary),
            "scores": json.dumps(scores)
        }, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"save_plan error: {e}")
        return False

def get_past_plans(user_id: str) -> list:
    try:
        response = requests.post(f"{TOOLBOX_URL}/tools/get-past-plans/invoke", json={
            "user_id": user_id
        }, timeout=10)
        if response.status_code == 200:
            return response.json().get("result", [])
        return []
    except Exception as e:
        print(f"get_past_plans error: {e}")
        return []

def get_user_preferences(user_id: str) -> dict:
    try:
        response = requests.post(f"{TOOLBOX_URL}/tools/get-user-preferences/invoke", json={
            "user_id": user_id
        }, timeout=10)
        if response.status_code == 200:
            result = response.json().get("result", [])
            if result:
                return result[0].get("preferences", {})
        return {}
    except Exception as e:
        print(f"get_user_preferences error: {e}")
        return {}

def save_user_preferences(user_id: str, preferences: dict) -> bool:
    try:
        response = requests.post(f"{TOOLBOX_URL}/tools/save-user-preferences/invoke", json={
            "user_id": user_id,
            "preferences": json.dumps(preferences)
        }, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"save_user_preferences error: {e}")
        return False
