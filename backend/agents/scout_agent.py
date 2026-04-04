import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from backend.tools.places_tool import find_spots

def create_scout_agent() -> LlmAgent:
    agent = LlmAgent(
        name="scout_agent",
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        description="Finds the best real-world spots for any activity at any location worldwide.",
        instruction=(
            "You are Scout, an expert at finding perfect venues for any activity anywhere in the world.\n\n"
            "Given a location, occasion, vibe, and budget - find real highly-rated spots using find_spots.\n\n"
            "For each plan call find_spots at least 3 times - once per slot: opening, main, closing.\n"
            "Only include spots rated 4.0 or above. Match the vibe and budget requested.\n"
            "Return a JSON with slots: opening, main, closing - each with top 2-3 spot options including name, address, rating, maps_link, notes."
        ),
        tools=[FunctionTool(find_spots)]
    )
    return agent
