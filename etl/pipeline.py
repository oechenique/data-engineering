from owslib.wfs import WebFeatureService
import geopandas as gpd
import pandas as pd
from datetime import datetime
import psycopg2
import os
from typing import Optional, List
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FIRMSPipeline:
   LAYER_TYPES = [
       "ms:fires_modis_24hrs",
       "ms:fires_modis_7days", 
       "ms:fires_noaa20_24hrs",
       "ms:fires_noaa20_7days",
       "ms:fires_noaa21_24hrs", 
       "ms:fires_noaa21_7days"
   ]

   REGIONS = {
       "Canada": "Canada",
       "Alaska": "Alaska", 
       "USA": "USA_contiguous_and_Hawaii",
       "Central_America": "Central_America",
       "South_America": "South_America",
       "Europe": "Europe",
       "North_Central_Africa": "Northern_and_Central_Africa",
       "Southern_Africa": "Southern_Africa",
       "Russia_Asia": "Russia_Asia",
       "South_Asia": "South_Asia",
       "SouthEast_Asia": "SouthEast_Asia",
       "Australia_NZ": "Australia_NewZealand"
   }

   def __init__(self):
       self.wfs_url = os.getenv("WFS_BASE_URL")
       self.api_key = os.getenv("API_KEY")
       self.db_conn = self._get_db_connection()
   
   def _get_db_connection(self):
       return psycopg2.connect(
           dbname=os.getenv("POSTGRES_DB"),
           user=os.getenv("POSTGRES_USER"),
           password=os.getenv("POSTGRES_PASSWORD"),
           host=os.getenv("POSTGRES_HOST", "db"),
           port=os.getenv("POSTGRES_PORT", "5432")
       )

   def fetch_region_data(self, region: str) -> Optional[gpd.GeoDataFrame]:
       try:
           wfs = WebFeatureService(
               url=f"{self.wfs_url}/{self.REGIONS[region]}/{self.api_key}/",
               version="2.0.0"
           )
           
           all_data = []
           for layer in self.LAYER_TYPES:
               try:
                   logger.info(f"Fetching {layer} for {region}")
                   response = wfs.getfeature(
                       typename=layer,
                       outputFormat="application/json"
                   )
                   data = json.loads(response.read())
                   gdf = gpd.GeoDataFrame.from_features(data['features'])
                   if not gdf.empty:
                       gdf["source"] = layer
                       gdf["region"] = region
                       all_data.append(gdf)
                       logger.info(f"Successfully fetched {len(gdf)} records")
               except Exception as e:
                   logger.warning(f"Error fetching layer {layer} for {region}: {e}")
                   continue
                   
           return pd.concat(all_data) if all_data else None
           
       except Exception as e:
           logger.error(f"Error processing region {region}: {e}")
           return None

   def preprocess_dataframe(self, gdf):
       """Convert data types for PostgreSQL compatibility"""
       try:
           # Convertir fechas
           gdf["acq_date"] = pd.to_datetime(gdf["acq_datetime"]).dt.date
           gdf["acq_datetime"] = pd.to_datetime(gdf["acq_datetime"])

           # Convertir valores numéricos
           gdf["confidence"] = pd.to_numeric(gdf["confidence"], errors="coerce").fillna(0).astype(int)
           gdf["brightness"] = pd.to_numeric(gdf["brightness"], errors="coerce")
           gdf["latitude"] = pd.to_numeric(gdf["latitude"], errors="coerce")
           gdf["longitude"] = pd.to_numeric(gdf["longitude"], errors="coerce")

           return gdf
       except Exception as e:
           logger.error(f"Error preprocessing dataframe: {e}")
           return gdf

   def load_to_database(self, gdf):
       """Insert data into PostgreSQL"""
       cur = self.db_conn.cursor()

       try:
           gdf = self.preprocess_dataframe(gdf)
           for _, row in gdf.iterrows():
               try:
                   cur.execute("""
                       INSERT INTO fires (
                           acquisition_date, acquisition_datetime, latitude, longitude, 
                           brightness, confidence, region, source, geom
                       ) VALUES (
                           %s, %s, %s, %s, %s, %s, %s, %s,
                           ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                       ) ON CONFLICT DO NOTHING
                   """, (
                       row["acq_date"], row["acq_datetime"],
                       row["latitude"], row["longitude"],
                       row["brightness"], row["confidence"],
                       row["region"], row["source"],
                       row["longitude"], row["latitude"]
                   ))
               except Exception as e:
                   logger.error(f"Error inserting row: {e}")
                   continue

           self.db_conn.commit()
           logger.info(f"Successfully committed {len(gdf)} records")
       except Exception as e:
           logger.error(f"Transaction failed: {e}")
           self.db_conn.rollback()
       finally:
           cur.close()

   def run(self):
       try:
           for region in self.REGIONS.keys():
               logger.info(f"Processing region: {region}")
               gdf = self.fetch_region_data(region)
               
               if gdf is not None:
                   self.load_to_database(gdf)
                   logger.info(f"Successfully loaded data for {region}")
               else:
                   logger.warning(f"No data obtained for {region}")

       except Exception as e:
           logger.error(f"Pipeline error: {e}")
       finally:
           self.db_conn.close()

if __name__ == "__main__":
   pipeline = FIRMSPipeline()
   pipeline.run()