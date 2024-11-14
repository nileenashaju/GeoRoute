import pandas as pd
from sqlalchemy import create_engine, text

# Database setup
engine = create_engine('postgresql://postgres:admin@localhost:1024/mydatabase')

# Load CSVs into the database
coords_df = pd.read_csv('latitude_longitude_details.csv')
terrain_df = pd.read_csv('terrain_classification.csv')
merged_df = pd.read_csv('merged_lat_lon_terrain.csv')

# Clean column names in the DataFrames
terrain_df.columns = terrain_df.columns.str.strip()
merged_df.columns = merged_df.columns.str.strip()




coords_df.to_sql('latitude_longitude_details', engine, if_exists='replace', index=False)
try:
    terrain_df.to_sql('terrain_classification', engine, if_exists='replace', index=False)
    merged_df.to_sql('merged_lat_lon_terrain', engine, if_exists='replace', index=False)
except Exception as e:
    print(f"Error inserting data: {e}")


# Define query

query = text("""
SELECT * 
FROM merged_lat_lon_terrain
WHERE "Terrain" LIKE '%road%' AND "Terrain" NOT LIKE '%civil station, road%';
""")


# Execute query using the engine
with engine.connect() as connection:
    result = connection.execute(query)
    rows = result.fetchall()
    print(rows)
