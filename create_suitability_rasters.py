#!C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
"""
GEOM3010 - Assignment 1 Habitat Analysis

By Dillon Chaffey, Oct ##, 2020
"""

from utils import *
from config import *

# CRITERIA
water_weight = 40
wetlands_weight = 0
fields_weight = 20
roads_weight = 20
fave_tree_weight = 10
forest_weight = 10

# Merge forest polygons, join descriptions from Forest_metadata_web_attrib.pdf, extract features and rasterize
forest_poly_M = arcpy.Merge_management([forest_poly1, forest_poly2], "#")

forest_poly_M_FC = arcpy.MakeFeatureLayer_management(in_features=forest_poly_M, out_layer="FOREST_POLY")

forest_poly_M_J = arcpy.AddJoin_management(forest_poly_M_FC, 'FORNON', forestFN_table, 'ID')
forest_poly_M_J = arcpy.AddJoin_management(forest_poly_M_FC, 'SP1', forestSP_table, 'ID')
forest_poly_M_J = arcpy.AddJoin_management(forest_poly_M_FC, 'WC_TYPE', forestWC_table, 'ID')

# *****************Use this when the tool doesn't output anything, use .save for rasters
forest_poly_M_J = arcpy.CopyFeatures_management(forest_poly_M_J, "#")

# # #####@TODO FIX BOGS
wetland_Q = "FOREST_WC1 = 'Lake Wetland' Or FOREST_WC1 = 'Wetlands General'"
# bog_Q = "FOREST_F_1 LIKE 'Open Bogs%' Or FOREST_F_1 LIKE 'Treed Bogs%'"
agriculture_Q = "FOREST_F_1 LIKE '%Agriculture%'"
fave_tree_Q = "FOREST_S_1 = 'Eastern Hemlock'"
second_fave_tree_Q = "FOREST_S_1 = 'Sugar Maple' Or FOREST_S_1 = 'Beech'"

wetlands_rast = query_and_rasterize(forest_poly_M_J, "FOREST_WC1", wetland_Q)
# bog_rast = query_and_rasterize(forest_poly_M_J, "FOREST_F_1", bog_Q) #query selects nothing
agriculture_rast = query_and_rasterize(forest_poly_M_J, "FOREST_F_1", agriculture_Q)
fave_tree_rast = query_and_rasterize(forest_poly_M_J, "FOREST_S_1", fave_tree_Q)
second_fave_tree_rast = query_and_rasterize(forest_poly_M_J, "FOREST_S_1", second_fave_tree_Q)

fave_tree_combo_rast = arcpy.sa.CellStatistics([fave_tree_rast, second_fave_tree_rast], "MAXIMUM", "DATA")
fave_tree_buf_rast = arcpy.sa.EucDistance(fave_tree_combo_rast, 200)

# extract and rasterize features from NSTDB
roads_dirt_Q = '''
   FEAT_DESC LIKE '%TRACK%' Or FEAT_CODE LIKE '%Unpaved%' Or FEAT_DESC LIKE '%RAILROAD%' 
   Or FEAT_DESC LIKE '%Abandoned%' Or FEAT_DESC LIKE '%WATER ACCESS%'
'''
water_line_Q = "FEAT_CODE LIKE 'WARV%'"
water_poly_Q = "FEAT_CODE NOT LIKE 'WASW40'"

roads_dirt_rast = query_and_rasterize(roads_line, "FEAT_CODE", roads_dirt_Q)
roads_dirt_buf_rast = arcpy.sa.EucDistance(roads_dirt_rast, 200)
water_line_rast = query_and_rasterize(water_line, "FEAT_CODE", water_line_Q)
water_poly_rast = query_and_rasterize(water_poly, "FEAT_CODE", water_poly_Q)
water_combo_rast = arcpy.sa.CellStatistics([water_line_rast, water_poly_rast], "MAXIMUM", "DATA")
water_buf_rast = arcpy.sa.EucDistance(water_combo_rast, 200)


# ("field_buf200.img" + "wat_buf200.img" + "rd_buf200.img")/3
# Deer_suit = ( ( 3 * "wt_buf_suit" ) + ( 2 * "fd_buf_suit" ) + ( 1 * "rd_buf_suit") ) / 6

# mean_buf = arcpy.sa.CellStatistics ([roads_dirt_buf_rast, water_buf_rast, fave_tree_buf_rast], "MEAN", "NODATA")
# mean_buf.save(out_hab_suit)

out_ras = arcpy.sa.Raster(water_buf_rast) * .5 + \
          arcpy.sa.Raster(roads_dirt_buf_rast) * .25 + \
          arcpy.sa.Raster(fave_tree_buf_rast) * .25
out_ras.save(HABITAT_SUIT_RAST)


# rd_suit_1 = ReclassByASCIIFile(roads_line_rast_buf, "rmt.txt", "DATA")
# print(rd_suit_1)

# rd_suit_2 = Con(IsNull(rd_suit_1), 10, "#", rd_suit_1) #ERROR what sql
# print(rd_suit_2)


# ######## WHY do these produce slightly different rasters
# out_ras = arcpy.sa.Raster(water_buf_rast) *.5 + arcpy.sa.Raster(roads_dirt_buf_rast) * .25 + arcpy.sa.Raster(fave_tree_buf_rast *.25)
# print(out_ras)
# out_ras.save('RC2.TIF')
# myWSumTable = arcpy.sa.WSTable([
#     [water_buf_rast, "VALUE", .5],
#     [roads_dirt_buf_rast, "VALUE", .25],
#     [fave_tree_buf_rast, "VALUE", .25]]
# )
#
# outWSumT = arcpy.sa.WeightedSum(myWSumTable)
#
# outWSumT.save("WO.TIF")







