# Proyecto Visualización Avanzada de Datos - VISDAT

#### Project for Advanced Data Visualization Course, Using Grafana for Dashboards, ClickHouse as Back and Python to load Data 

## Original Datasets

### World Energy Consumption

https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption

### Dataset ISO:

https://www.kaggle.com/datasets/petersorensen360/iso3166countrieswithregionalcodes

We use ISO Codes in order to use ISO codes to get flags and use maps in Grafana. 

## Steps to deploy

1 - Clone this repository

2 - Go to the project folder and run:

```bash 
docker-compose up -d
```

3 - Load data into ClickHouse using the provided Python script:

```bash
python scripts/load_data.py
```
* Make sure you have the required Python packages installed. You can install them using pip:

```bash
pip install pandas clickhouse-connect
```

* Built for Python 3.8 and above.

4 - Access Grafana at `http://localhost:3000` (default credentials: admin/thisIsNotASecurePassword1234).