# 🔥 FIRMS Data Engineering Pipeline 🌍

**Real-time global wildfire monitoring** using **automated ETL, spatial databases with PostGIS, a scalable API with FastAPI, and an interactive web frontend powered by Leaflet.**

## 📌 Key Features

✅ **Automated data ingestion** from NASA FIRMS every 15 minutes.  
✅ **Efficient storage** in PostgreSQL/PostGIS with spatial indexing.  
✅ **Optimized API with FastAPI** for GeoJSON queries, time-based filtering, and spatial searches.  
✅ **Real-time visualization** using Leaflet on a simple yet effective web interface.  
✅ **Deployment via Docker** for easy replication and scalability.  

## 🏗️ Architecture

📡 **ETL:** Fetches and transforms FIRMS data → Stores in PostGIS.  
🛰️ **PostGIS:** Spatial database optimized for geospatial queries.  
🚀 **FastAPI API:** Serves data with filters by date, region, and more.  
🌍 **Leaflet Web App:** Displays real-time wildfire data interactively.  
🐳 **Docker Compose:** Manages the entire infrastructure for easy deployment.  

```plaintext
[FIRMS WFS API] -> [ETL Pipeline] -> [PostgreSQL + PostGIS] -> [FastAPI] -> [Web UI]
                   (Python/Pandas)     (Spatial Database)     (REST API)  (Leaflet)
```

## ⚙️ Installation & Usage

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/[username]/firms-pipeline.git
cd firms-pipeline
```

2️⃣ **Run everything with Docker**  
```bash
docker-compose up -d
```

3️⃣ **Access the API and Web Interface**  
- **API Documentation:** `http://localhost:8001/docs`  
- **Web Map:** `http://localhost:8080/`  

## 🌐 API Reference

Example: Fetch wildfires from the last 24 hours in GeoJSON format.  
```bash
curl http://localhost:8001/fires/recent?hours=24
```

## 🚀 Scalability & Future Enhancements

🔹 **Big Data Support:** Scale with Kubernetes or Airflow.  
🔹 **Machine Learning Predictions:** Detect wildfire patterns using ML models.  
🔹 **PostGIS Optimization:** Indexing and partitioning for large datasets.  
🔹 **Interactive Dashboard:** Advanced analytics with charts and statistics.  

## 💻 Tech Stack | 技術スタック
- **Backend**: Python, FastAPI, GeoPandas
- **Database**: PostgreSQL, PostGIS
- **Frontend**: Leaflet.js, HTML/CSS
- **Infrastructure**: Docker, Docker Compose

## Let's Connect! 一緒に学びましょう 🌐

[![Twitter Badge](https://img.shields.io/badge/-@GastonEchenique-1DA1F2?style=flat&logo=x&logoColor=white&link=https://x.com/GastonEchenique)](https://x.com/GastonEchenique)
[![LinkedIn Badge](https://img.shields.io/badge/-Gastón_Echenique-0A66C2?style=flat&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/gaston-echenique/)](https://www.linkedin.com/in/gaston-echenique/)
[![GitHub Badge](https://img.shields.io/badge/-oechenique-333?style=flat&logo=github&logoColor=white&link=https://github.com/oechenique)](https://github.com/oechenique)
[![GeoAnalytics Badge](https://img.shields.io/badge/-GeoAnalytics_Site-2ecc71?style=flat&logo=google-earth&logoColor=white&link=https://oechenique.github.io/geoanalytics/)](https://oechenique.github.io/geoanalytics/)
[![Discord Badge](https://img.shields.io/badge/-Gastón|ガストン-5865F2?style=flat&logo=discord&logoColor=white&link=https://discord.com/users/gastonechenique)](https://discord.com/users/gastonechenique)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/rhrqmdyaig)

🔥 **This pipeline is more than an ETL; it's a production-ready geospatial data infrastructure.**  
Designed for **Data Engineers and GIS enthusiasts** to analyze real-time wildfire data. 🌎📡