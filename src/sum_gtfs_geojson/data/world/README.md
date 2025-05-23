The file `` contains country limitations. 
This is usefull when handling geolocations for a Living Lab that crosses the country border, for instance Geneva public transport network includes stops in France. 

Source file : [https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip](https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip)

The file is read by `geopandas` library 

```py
import geopandas as gpd
from shapely.geometry import Point

# Load world country boundaries
world = gpd.read_file("data/world/10m/ne_10m_admin_0_countries.shp")

# Select the country of interest, e.g., France
country_name = "France"
country = world[world.name == country_name]

# Sample data
data = pd.DataFrame({
    'latitude': [48.8566, 50.8503, 45.7640],  # Paris, Brussels, Lyon
    'longitude': [2.3522, 4.3517, 4.8357]
})

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
geo_data = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

# Ensure Coordinate Reference Systems Match
if geo_data.crs != country.crs:
    geo_data = geo_data.to_crs(country.crs)


# Filter the data 
filtered_data = geo_data[geo_data.within(country.unary_union)]

```