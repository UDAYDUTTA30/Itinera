import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host=os.getenv("ALLOYDB_HOST", "127.0.0.1"),
            port=int(os.getenv("ALLOYDB_PORT", "5432")),
            database=os.getenv("ALLOYDB_DATABASE", "itinera_db"),
            user=os.getenv("ALLOYDB_USER", "postgres"),
            password=os.getenv("ALLOYDB_PASSWORD", ""),
            min_size=1,
            max_size=10,
        )
    return _pool

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
