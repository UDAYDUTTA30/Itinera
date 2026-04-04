import os
from google.adk.agents import LlmAgent

def create_planner_agent() -> LlmAgent:
    agent = LlmAgent(
        name="planner_agent",
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        description="Builds a realistic timed validated itinerary from scout and transit data.",
        instruction=(
            "You are Planner, expert at crafting beautiful realistic itineraries for any occasion worldwide.\n\n"
            "Given spots from Scout and transport from Transit - build a complete timed itinerary.\n\n"
            "Templates:\n"
            "- Lunch date: cafe (45min) -> walk (20min) -> restaurant (90min) -> dessert (30min)\n"
            "- Dinner date: bar/rooftop (45min) -> restaurant (90min) -> nightcap (45min)\n"
            "- Business meeting: coffee (30min) -> main venue (90min) -> debrief (30min)\n"
            "- Evening outing: sunset spot (30min) -> dinner (90min) -> drinks (60min)\n"
            "- Family trip: morning attraction -> lunch -> afternoon activity -> early dinner\n"
            "- Solo exploration: cafe -> landmark -> market -> sunset spot\n\n"
            "Validate: travel times realistic, budget adds up, no backtracking in route.\n\n"
            "Score 1-10: vibe_match, coherence, practicality.\n\n"
            "Return complete itinerary JSON with title, date, location, summary, stops[], transport_legs[], scores{}, total_estimated_cost."
        )
    )
    return agent
