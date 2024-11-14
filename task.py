import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from geopy.distance import geodesic


# Load and process CSV data to fix discontinuities
def process_coordinates(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Set a threshold for latitude and longitude differences
    discontinuity_threshold = 0.01  # Adjust this value as needed

    data['discontinuity'] = (data[['latitude', 'longitude']].diff().abs() > discontinuity_threshold).any(axis=1)

    # Correct discontinuous points using linear interpolation
    corrected_data = data.copy()
    for i in range(1, len(data) - 1):
        if data.loc[i, 'discontinuity']:
            corrected_data.loc[i, 'latitude'] = (data.loc[i - 1, 'latitude'] + data.loc[i + 1, 'latitude']) / 2
            corrected_data.loc[i, 'longitude'] = (data.loc[i - 1, 'longitude'] + data.loc[i + 1, 'longitude']) / 2

    # Save corrected data to a new CSV
    corrected_data.drop(columns=['discontinuity'], inplace=True)
    corrected_data.to_csv('corrected_coordinates.csv', index=False)
    return data, corrected_data


# Plotting the coordinates on a map for comparison
def plot_coordinates(original_data, corrected_data):
    # Create GeoDataFrames from latitude and longitude data
    original_gdf = gpd.GeoDataFrame(
        original_data, geometry=[Point(xy) for xy in zip(original_data['longitude'], original_data['latitude'])],
        crs="EPSG:4326"
    )
    corrected_gdf = gpd.GeoDataFrame(
        corrected_data, geometry=[Point(xy) for xy in zip(corrected_data['longitude'], corrected_data['latitude'])],
        crs="EPSG:4326"
    )

    # Create subplots with basemaps for better visualization
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))

    # Original path plot
    original_gdf.plot(ax=ax[0], color='red', markersize=5, label="Original Path")
    ax[0].set_title("Original Path")
    ax[0].set_xlabel("Longitude")
    ax[0].set_ylabel("Latitude")
    ctx.add_basemap(ax[0], crs=original_gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik)

    # Corrected path plot
    corrected_gdf.plot(ax=ax[1], color='green', markersize=5, label="Corrected Path")
    ax[1].set_title("Corrected Path")
    ax[1].set_xlabel("Longitude")
    ax[1].set_ylabel("Latitude")
    ctx.add_basemap(ax[1], crs=corrected_gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik)

    plt.legend()
    plt.show()


# Laod both csv file and merge based on distance
import pandas as pd
from geopy.distance import geodesic


def merge_lat_lon_terrain(lat_lon_csv, terrain_csv, output_csv):
    # Load the latitude-longitude CSV file
    lat_lon_data = pd.read_csv(lat_lon_csv)

    # Calculate cumulative distance for lat-lon data
    lat_lon_data['KM'] = 0.0  # Initialize the distance column
    for i in range(1, len(lat_lon_data)):
        point_a = (lat_lon_data.iloc[i - 1]['latitude'], lat_lon_data.iloc[i - 1]['longitude'])
        point_b = (lat_lon_data.iloc[i]['latitude'], lat_lon_data.iloc[i]['longitude'])
        distance = geodesic(point_a, point_b).kilometers
        lat_lon_data.at[i, 'KM'] = lat_lon_data.at[i - 1, 'KM'] + distance

    # Load the terrain CSV file
    terrain_data = pd.read_csv(terrain_csv)
    terrain_data = terrain_data.rename(columns={'distance (in km)': 'KM'})

    # Merge based on the nearest distance in KM
    lat_lon_data['Terrain'] = lat_lon_data['KM'].apply(
        lambda x: terrain_data.iloc[(terrain_data['KM'] - x).abs().argsort()[:1]]['terrain'].values[0]
    )

    # Save the merged data to a new CSV file
    lat_lon_data.to_csv(output_csv, index=False)
    print("Merged data saved to:", output_csv)


# Main script execution
if __name__ == "__main__":
    # Load and process coordinates
    original_data, corrected_data = process_coordinates('latitude_longitude_details.csv')

    # Merge both csv files(latitude_longitude_details.csv,terrain_classification.csv)
    merge_lat_lon_terrain('latitude_longitude_details.csv', 'terrain_classification.csv', 'merge_lat_lon_terrain.csv')

    # Plot original and corrected data
    plot_coordinates(original_data, corrected_data)
