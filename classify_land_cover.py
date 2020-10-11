#!C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
"""
GEOM3010 - Assignment 1 Habitat Analysis

Outputs a classified land cover raster
Requires a landsat tile and a .gsg signature file

By Dillon Chaffey, Oct ##, 2020
"""

import os
import arcpy

aoi_poly        = "StudyAreaBoundary.shp"
ls_MS           = "LC80090292015171LGN00_MTL.txt"
ls_pan          = "LC80090292015171LGN00_B8.TIF"
sigs_shp        = "Landcover_Training_Areas.shp"

OUT_CLASSIFIED_RASTER = "LAND_COVER.TIF"

cur_dir = os.path.dirname(__file__)
arcpy.env.workspace = cur_dir + '/data/'
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = SW = cur_dir + '/temp/'

for row in arcpy.da.SearchCursor(aoi_poly, ['Name', 'SHAPE@']):
    if row[0] == "Dillon":
        arcpy.env.extent = row[1].extent

ls_MS_C = arcpy.CopyRaster_management(in_raster=ls_MS, out_rasterdataset="#")

ls_pan_C = arcpy.CopyRaster_management(in_raster=ls_pan, out_rasterdataset="#")

ls_MS_C_P = arcpy.CreatePansharpenedRasterDataset_management(
    in_raster=ls_MS_C,
    red_channel=3,
    green_channel=2,
    blue_channel=1,
    infrared_channel=4,
    in_panchromatic_image=ls_pan_C,
)
print(ls_MS_C_P)

sigs = arcpy.sa.CreateSignatures(
    in_raster_bands=ls_MS_C_P,
    in_sample_data=sigs_shp,
    sample_field='Classvalue',
    out_signature_file="#"
)

# classed_rast = arcpy.ia.MLClassify(arcpy.sa.Raster(ls_MS_C_P), sigs)
# result = classed_rast.save('CLASSED.tif')
#
# result = arcpy.sa.ClassProbability(
#     in_raster_bands=ls_MS_C_P,
#     in_signature_file=sigs
# )
#
# print(result)
#
#
#
# for i in range(arcpy.GetMessageCount()):
#   print(arcpy.GetMessage(i))
#
#
# # input("Press enter to exit")