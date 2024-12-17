import numpy as np
from osgeo import osr
import pyproj


#Function Definition
def geo2proj(lons, lats, current_epsg = 4326, target_epsg = 4326):
    """
    Converts geographic coordinates (lon, lat) to projected coordinates (x, y)
    
    INPUT
    lons: array of longitudes
    lats: array of latitudes
    current_epsg: epsg code of geographic coordintes - default: 4326 (WGS84)
    target_epsg:  epsg code of target projected coordinates - default: 32616 (UTM zone 16N Meters)
    
    OUTPUT
    nx2 array of converted coordinates in x, y order
    """

    #Create Transformation
    source_epsg = f'epsg:{current_epsg}'
    target_epsg = f'epsg:{target_epsg}'
    ct = pyproj.Transformer.from_crs(source_epsg,target_epsg)

    # Convert to target crs
    x, y = ct.transform(lats,lons)
        
    return x, y