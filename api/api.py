from fastapi import FastAPI
import psycopg2
import os
from database import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FIRMS API"}

@app.get("/fires/")
def get_fires():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, acquisition_date, latitude, longitude, brightness, confidence, region 
        FROM fires 
        LIMIT 10;
    """)
    columns = [desc[0] for desc in cur.description]
    fires = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return {"fires": fires}

@app.get("/fires/recent")
def get_recent_fires(hours: int = 24):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT acquisition_date, acquisition_datetime, latitude, longitude, brightness, confidence, region, source
        FROM fires
        WHERE acquisition_datetime >= NOW() - INTERVAL %s
        ORDER BY acquisition_datetime DESC
    """, (f'{hours} hours',))

    columns = [desc[0] for desc in cur.description]
    results = [dict(zip(columns, row)) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return {"fires": results}