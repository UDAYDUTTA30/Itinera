import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from backend.tools.routes_tool import get_transit_options

def create_transit_agent() -> LlmAgent:
    agent = LlmAgent(
        name="transit_agent",
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        description="Calculates realistic transport options between locations anywhere in the world.",
        instruction=(
            "You are Transit, an expert at finding the best ways to get between places worldwide.\n\n"
            "Given a list of stops - calculate transport between each consecutive pair using get_transit_options.\n"
            "Try TRANSIT first, then WALK if under 1km, always include a cab fallback.\n"
            "Add practical city-specific travel tips. Keep travel under 30 min per leg where possible.\n"
            "Return structured JSON with transport legs between each stop pair."
        ),
        tools=[FunctionTool(get_transit_options)]
    )
    return agent
