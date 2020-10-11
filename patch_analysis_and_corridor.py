#!C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
"""
GEOM3010 - Assignment 1 Habitat Analysis

By Dillon Chaffey, Oct ##, 2020
"""

from arcpy.sa import *

from utils import *
from config import *

# hexes = arcpy.GenerateTessellation_management("#", arcpy.da.Describe(aoi_poly)['extent'], "HEXAGON", "30 Hectares")
#
# arcpy.management.CalculateField(hexes, "Id", "!FID! + 1", "PYTHON3", '', "TEXT")
#
# hexes_rast = arcpy.FeatureToRaster_conversion(in_features=hexes, field="Id", cell_size=10)
#
# #this looks different than the pdf
# hexes_rast_zone_stats = ZonalStatistics(hexes_rast, "Value", HABITAT_SUIT_RAST, "MEAN", "DATA")
#
# hab_patches_GT_85 = Con(hexes_rast_zone_stats, 1, "", "Value <= 85")
#
# hab_clusters = RegionGroup(hab_patches_GT_85)
#
# biggest_patch = 0
# biggest_patch_value = 0
# second_biggest_patch = 0
# rows = arcpy.SearchCursor(hab_clusters)
# for row in rows:
#     # print(str(row.getValue("VALUE")) +" "+ str(row.getValue("COUNT")))
#     if row.getValue("COUNT") > biggest_patch_value:
#         second_biggest_patch = biggest_patch
#         biggest_patch, biggest_patch_value = row.getValue("VALUE"), row.getValue("COUNT")
#
# biggest_cluster = ExtractByAttributes(hab_clusters, "Value = " + str(biggest_patch))
# second_biggest_cluster = ExtractByAttributes(hab_clusters, "Value = " + str(second_biggest_patch))
# #print(biggest_cluster, second_biggest_cluster)
#
roads_paved_Q = "FEAT_DESC NOT LIKE '%Unpaved%' And FEAT_DESC NOT LIKE '%TRACK%' And FEAT_DESC NOT LIKE '%DRIVEWAY%'"
roads_paved_rast = query_and_rasterize(roads_line, "FEAT_CODE", roads_paved_Q)

roads_paved_buf = EucDistance(roads_paved_rast)
roads_paved_remap = RemapRange([
    [0,1.0,1000],
    [1.0,100.0,500],
    [100.0,150.0,100],
    [150.0,250.0,50],
    [250.0,20000.0,1]
])

roads_paved_remapped = ReclassByASCIIFile(roads_paved_buf, "PAVED_ROAD_COR_IMP.TXT", "DATA")
roads_paved_buf_remapped = arcpy.da.Describe(roads_paved_remapped)["catalogPath"]
roads_paved_remapped.save()

ReclassByASCIIFile("water_suit_tmp.img", "WATER_REMAP.TXT")


# roads_paved_remapped = Reclassify(r"C:\GEOS_COURSEWORK\GEOM3020_APPLIED\HABBO\temp\Feature_RR_ROAD1.tif", "VALUE", roads_paved_remap)
# roads_paved_remapped = ReclassByASCIIFile(roads_paved_buf, "VALUE", "PAVED_ROAD_COR_IMP.TXT")
# print(roads_paved_remapped)

