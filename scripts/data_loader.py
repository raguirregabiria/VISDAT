#!/usr/bin/env python3
"""
Data Loader Script for ClickHouse Database
Converts notebook.ipynb functionality into a standalone Python script
"""

# Import required libraries
import yaml
import clickhouse_connect
import pandas as pd
import os

def load_config_from_docker_compose():
    """Load ClickHouse configuration from docker-compose.yml"""
    print("Loading configuration from docker-compose.yml...")
    
    with open("docker-compose.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    ch_user = cfg['services']['clickhouse']['environment']['CLICKHOUSE_USER']
    ch_password = cfg['services']['clickhouse']['environment']['CLICKHOUSE_PASSWORD']
    
    return ch_user, ch_password

def create_database(client):
    """Create the datasets database if it doesn't exist"""
    print("Creating database if not exists...")
    client.command("CREATE DATABASE IF NOT EXISTS datasets")

def execute_sql_files(client):
    """Execute all SQL files from the sql/ folder"""
    print("Executing SQL files...")
    
    folder = "sql/"
    for sql_file in os.listdir(folder):
        print(f"Executing {sql_file}...")
        with open(folder + sql_file) as f:
            string_file = f.read()
        client.command(string_file)

def load_world_energy_data(client):
    """Load and process world energy consumption data"""
    print("Loading world energy consumption data...")
    
    # Load and filter data (from 1980 onwards)
    df = pd.read_csv("datasets/world_energy_consumption.csv")
    df = df[df["year"] > 1980]
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    # Verify DataFrame structure
    print("Columns:", df.columns.tolist())
    print("Shape:", df.shape)

    # Convert data types
    df['population'] = df['population'].astype('UInt64')
    df['iso_code'] = df['iso_code'].astype('str')
    df['country'] = df['country'].astype('str')

    # Insert data into ClickHouse
    print("Inserting world energy data into ClickHouse...")
    client.insert_df('datasets.world_energy_consumption', df)
    print("World energy data inserted successfully!")

def load_iso_country_data(client):
    """Load and process ISO country codes data"""
    print("Loading ISO country codes data...")
    
    # Load ISO country data
    df_iso = pd.read_csv("datasets/ISO-3166-Countries-with-Regional-Codes.csv", na_filter=None)
    
    # Select and rename columns
    df_iso = df_iso[["name", "alpha-2", "alpha-3"]]
    df_iso.columns = ["name", "iso_2", "iso_3"]
    
    print("ISO DataFrame info:")
    print(df_iso.head())
    print("Data types:", df_iso.dtypes)
    
    # Insert data into ClickHouse
    print("Inserting ISO country data into ClickHouse...")
    client.insert_df("datasets.iso_country", df_iso)
    print("ISO country data inserted successfully!")

def main():
    """Main function to orchestrate the data loading process"""
    print("Starting data loading process...")
    
    try:
        # Load configuration
        ch_user, ch_password = load_config_from_docker_compose()
        
        # Connect to ClickHouse
        print("Connecting to ClickHouse...")
        client = clickhouse_connect.get_client(host='localhost', username=ch_user, password=ch_password)
        
        # Create database
        create_database(client)
        
        # Execute SQL files to create tables
        execute_sql_files(client)
        
        # Load world energy data
        load_world_energy_data(client)
        
        # Load ISO country data
        load_iso_country_data(client)
        
        print("Data loading process completed successfully!")
        
    except Exception as e:
        print(f"Error occurred during data loading: {e}")
        raise

if __name__ == "__main__":
    main()