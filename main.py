from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Establecer conexión con PostgreSQL."""
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

@app.get("/")
def home():
    return {"message": "🔥 FIRMS API is running!"}

@app.get("/fires")
def get_fires():
    """Obtener datos de incendios almacenados en PostgreSQL."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', COALESCE(json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(geom)::json,
                        'properties', json_build_object(
                            'brightness', brightness,
                            'confidence', confidence,
                            'acquisition_date', acquisition_date,
                            'region', region
                        )
                    )
                ), '[]'::json)
            )
            FROM fires
            LIMIT 1000;
        """)
        geojson = cur.fetchone()[0]
        return JSONResponse(content=geojson)
    finally:
        cur.close()
        conn.close()

@app.get("/fires/recent")
async def get_recent_fires(hours: int = 24):
    """Obtener incendios recientes en formato GeoJSON."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', COALESCE(json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(geom)::json,
                        'properties', json_build_object(
                            'brightness', brightness,
                            'confidence', confidence,
                            'acquisition_date', acquisition_date,
                            'region', region
                        )
                    )
                ), '[]'::json)
            )
            FROM fires
            WHERE acquisition_date >= NOW() - INTERVAL '%s hours'
        """, (hours,))
        
        geojson = cur.fetchone()[0]
        return JSONResponse(content=geojson)
    finally:
        cur.close()
        conn.close()