import asyncpg
from fastapi import FastAPI

DATABASE_URL = "postgresql://pzw:pzw@localhost:5432/pzw"

app = FastAPI()


@app.get("/health")
async def health():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        version = await conn.fetchval("SELECT version()")
    finally:
        await conn.close()
    return {"status": "ok", "database": version}
