import os
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from backend.agents.scout_agent import create_scout_agent
from backend.agents.transit_agent import create_transit_agent
from backend.agents.planner_agent import create_planner_agent

def create_orchestrator() -> LlmAgent:
    scout = create_scout_agent()
    transit = create_transit_agent()
    planner = create_planner_agent()

    orchestrator = LlmAgent(
        name="itinera_orchestrator",
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        description="Primary orchestrator for Itinera - coordinates all sub-agents to produce a complete activity plan.",
        instruction=(
            "You are Itinera, a world-class AI activity organizer. Help people plan any activity anywhere in the world.\n\n"
            "Workflow:\n"
            "1. PARSE: Extract location, occasion, vibe, budget, group size, date, constraints from user message\n"
            "2. SCOUT: Call scout_agent to find real spots\n"
            "3. TRANSIT: Call transit_agent to get transport between spots\n"
            "4. PLAN: Call planner_agent to build the final timed itinerary\n"
            "5. RESPOND: Return a warm natural response with the itinerary JSON\n\n"
            "Handle follow-ups:\n"
            "- Regeneration requests (more romantic, avoid crowds) -> re-run with updated constraints\n"
            "- Save to calendar -> return calendar events\n"
            "- Change a stop -> replace just that stop\n\n"
            "Always return a plan. If no results found suggest nearby alternatives."
        ),
        tools=[
            AgentTool(scout),
            AgentTool(transit),
            AgentTool(planner)
        ]
    )
    return orchestrator
