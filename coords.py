import geopandas as gpd
import pandas as pd

# Load the original ABS SA3 boundary file
boundaries = gpd.read_file(
    "data/SA3_2021_AUST_GDA2020.shp"
)

# Check that the file has a coordinate reference system
print("CRS:", boundaries.crs)
print("Columns:", boundaries.columns.tolist())

if boundaries.crs is None:
    raise ValueError(
        "The boundary file has no CRS. "
        "Set the correct CRS before calculating coordinates."
    )

# Keep the SA3 identifier and name
boundaries = boundaries[
    ["SA3_CODE21", "SA3_NAME21", "geometry"]
].copy()

# Convert codes to strings so they can be joined consistently
boundaries["SA3_CODE21"] = (
    boundaries["SA3_CODE21"].astype(str)
)

# Project into an Australian projected coordinate system
# before calculating representative points
projected = boundaries.to_crs("EPSG:3577")

# Generate a point inside each SA3 polygon
representative_points = (
    projected.geometry.representative_point()
)

points = gpd.GeoDataFrame(
    projected[["SA3_CODE21", "SA3_NAME21"]].copy(),
    geometry=representative_points,
    crs=projected.crs
)

# Convert points to geographic coordinates
# EPSG:4326 uses longitude and latitude
points = points.to_crs("EPSG:4326")

# Extract coordinates into ordinary columns
points["Longitude"] = points.geometry.x
points["Latitude"] = points.geometry.y

# Export the coordinates without the geometry column
points[
    ["SA3_CODE21", "SA3_NAME21", "Longitude", "Latitude"]
].to_csv(
    "data/sa3_points.csv",
    index=False
)

print("Coordinate file created: data/sa3_points.csv")
print(points.head())