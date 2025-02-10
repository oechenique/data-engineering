CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS fires (
    id SERIAL PRIMARY KEY,
    acquisition_date DATE,
    acquisition_datetime TIMESTAMP WITH TIME ZONE,
    latitude FLOAT,
    longitude FLOAT,
    brightness FLOAT,
    confidence INTEGER,
    region TEXT,
    source VARCHAR(50),
    geom GEOMETRY(Point, 4326)
);

CREATE INDEX IF NOT EXISTS idx_fires_geom ON fires USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_fires_date ON fires(acquisition_date);