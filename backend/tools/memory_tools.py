import json
from backend.db.connection import get_pool

async def save_plan(user_id: str, query: str, intent: dict, itinerary: dict, scores: dict):
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO users (id) VALUES ($1) ON CONFLICT (id) DO NOTHING;", user_id)
            await conn.execute(
                "INSERT INTO plans (user_id, query, intent, itinerary, scores) VALUES ($1, $2, $3, $4, $5);",
                user_id, query, json.dumps(intent), json.dumps(itinerary), json.dumps(scores)
            )
        return True
    except Exception as e:
        print(f"save_plan error: {e}")
        return False

async def get_user_preferences(user_id: str) -> dict:
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT preferences FROM users WHERE id = $1", user_id)
            if row:
                return json.loads(row["preferences"]) if isinstance(row["preferences"], str) else dict(row["preferences"])
            return {}
    except Exception as e:
        print(f"get_user_preferences error: {e}")
        return {}

async def get_past_plans(user_id: str, limit: int = 5) -> list:
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT query, itinerary, created_at FROM plans WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2",
                user_id, limit
            )
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"get_past_plans error: {e}")
        return []
