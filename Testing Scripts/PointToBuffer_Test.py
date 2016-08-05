#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pmckinney
#
# Created:     19/07/2016
# Copyright:   (c) pmckinney 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

try:

    # would be user entered
    # need to try to convert to float
    # need to test type of
    # if not number, then add arcpy error
    # do nothing else
    lat = 40.2015
    lon = -77.1901
    # WGS 1984
    srWGS84 = arcpy.SpatialReference(4326)

    # create point
    point = arcpy.Point(lon, lat)

    # create geometry point
    geometryPoint = arcpy.PointGeometry(point, srWGS84)

    #print "Latitude = {}. Longitude = {}".format(geometryPoint.centroid.Y, geometryPoint.centroid.X)

    srNAD83 = arcpy.SpatialReference(2272)
    outputNAD83 = r'\\CCPASR07\ncgs$\Scripts\ArcGIS Geoprocessing\SARA Tool\SARA_Tool_DEV.gdb\InputPoint_NAD83'

    # Convert WGS 1984 layer to a NAD 1983 layer
    arcpy.Project_management(geometryPoint, outputNAD83, srNAD83, "NAD_1983_To_WGS_1984_1", preserve_shape = "PRESERVE_SHAPE")

    #output
    output = r'\\CCPASR07\ncgs$\Scripts\ArcGIS Geoprocessing\SARA Tool\SARA_Tool_DEV.gdb\MultiRing_NAD83'
    # create buffer
    arcpy.MultipleRingBuffer_analysis(outputNAD83, output, [1.5, 2], 'miles')

    print "Reprojected input lat/long into NAD 83 State Plane South PA. \n"
    print "created multiple buffers for input lat/long"

except Exception:
    e = sys.exc_info()[1]
    print(str(e.args[0]))