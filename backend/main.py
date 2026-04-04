import os
import uuid
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted
from backend.models.intent import QueryRequest, QueryResponse
from backend.tools.memory_tools import save_plan, get_past_plans
from backend.tools.calendar_tool import create_calendar_events

load_dotenv("backend/.env")

app = FastAPI(title="Itinera API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = None

@app.on_event("startup")
async def startup():
    global orchestrator
    from backend.agents.orchestrator import create_orchestrator
    orchestrator = create_orchestrator()
    print("Itinera orchestrator ready.")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "itinera-api"}

@retry(
    retry=retry_if_exception_type(ResourceExhausted),
    wait=wait_exponential_jitter(initial=2, max=30),
    stop=stop_after_attempt(5)
)
async def run_agent(runner, user_id, session_id, user_message):
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = event.content.parts[0].text
    return response_text

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())

        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai.types import Content, Part

        session_service = InMemorySessionService()
        runner = Runner(
            agent=orchestrator,
            app_name="itinera",
            session_service=session_service
        )

        await session_service.create_session(
            app_name="itinera",
            user_id=request.user_id,
            session_id=session_id
        )

        user_message = Content(parts=[Part(text=request.message)])
        response_text = await run_agent(runner, request.user_id, session_id, user_message)

        itinerary = None
        try:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                itinerary = json.loads(response_text[start:end])
                save_plan(
                    user_id=request.user_id,
                    query=request.message,
                    itinerary=itinerary,
                    scores=itinerary.get("scores", {})
                )
        except Exception:
            pass

        return QueryResponse(
            response=response_text,
            itinerary=itinerary,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calendar")
async def save_to_calendar(itinerary: dict):
    try:
        result = create_calendar_events(itinerary)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/plans/{user_id}")
async def get_plans(user_id: str):
    try:
        plans = get_past_plans(user_id)
        return {"plans": plans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
