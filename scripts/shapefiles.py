import geopandas as gpd

# Read a shapefile into a GeoDataFrame
gdf = gpd.read_file(r"C:\Users\kiun\Downloads\gea_mappings_and_shapefiles\gea_shapefiles\transgrp\transgrp.shp")

# Print the GeoDataFrame
print(gdf)