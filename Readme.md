# GeoRoute

find the latitude and longitude coordinates that are out of continous line and automatically fix the same to form a continuous path and save the final result to a 
separate csv file. Plot the coordinates in a map to show the before and after comparison 

## Requirements
* pandas==2.2.3
* geopandas==1.0.1
* geopy
* sqlalchemy
* pandas
* shapely

Install the required dependencies using:



```commandline
pip install -r requirements.txt
```

## CSV Files
* latitude_longitude_details.csv: Contains the latitude and longitude points with their respective terrain.
* terrain_classification.csv: Contains the terrain types and their corresponding distances in kilometers.

## Setup
1. Prepare CSV Files:
    * Ensure your latitude_longitude_details.csv and terrain_classification.csv files are formatted correctly and available in the project directory.

2. Set Up PostgreSQL Database:
    * Create a PostgreSQL database if you haven't already
    * Update the database connection string in the script ('postgresql://username:password@localhost:1024/mydatabase') with your actual PostgreSQL credentials.

   ## RUN
   Run the Script:
    * The main script reads the CSV files, calculates the cumulative distances, classifies the terrain.
       To run this code
        ```
      python task.py
      ```
     ![coordinates and corrected cordinates](images/map.png)
     ![execution](images/execution.png)

    * The second script is to load the csv files into PostgreSQL and query from the table, list all the points with terrain “road” in it without “civil station”.
     To run this code
        ```
      python loaddata.py
      ```
     ![postgress](images/postgress.png)

