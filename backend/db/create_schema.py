import asyncio
import asyncpg
import os

async def main():
    conn = await asyncpg.connect(
        host=os.getenv("ALLOYDB_HOST", "10.20.0.2"),
        port=int(os.getenv("ALLOYDB_PORT", "5432")),
        database="postgres",
        user="postgres",
        password=os.getenv("ALLOYDB_PASSWORD", "Itinera@2026")
    )
    
    await conn.execute("CREATE DATABASE itinera_db;")
    print("Database created.")
    await conn.close()
    
    conn = await asyncpg.connect(
        host=os.getenv("ALLOYDB_HOST", "10.20.0.2"),
        port=int(os.getenv("ALLOYDB_PORT", "5432")),
        database="itinera_db",
        user="postgres",
        password=os.getenv("ALLOYDB_PASSWORD", "Itinera@2026")
    )
    
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            preferences JSONB DEFAULT \'{}\',
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id TEXT,
            query TEXT,
            intent JSONB,
            itinerary JSONB,
            scores JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            messages JSONB DEFAULT \'[]\',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)
    print("Schema created successfully.")
    await conn.close()

asyncio.run(main())
