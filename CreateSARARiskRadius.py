#----------------------------------------------------------------------------------------------#
# Name:        Create SARA Risk Radii
#
# Purpose:     Create risk radii for a user selected SARA facility
#
# Summary:     User enters the latitude, longitude, and PATTS ID for the facility.  User also
#              enters the distances and units for the risk radii.
#
# Author:      Patrick McKinney
# Created:     07/26/2016
# Updated:
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#----------------------------------------------------------------------------------------------#

# access ArcPy module
import arcpy

# User entered variables from ArcGIS tool
# user entered latitude
lat = arcpy.GetParameterAsText(0)
# user entered longitude
lon = arcpy.GetParameterAsText(1)
# PATTS ID
pattsID = arcpy.GetParameterAsText(2)
# Buffer distances
mrbDistances = arcpy.GetParameterAsText(3)
# Buffer units - will typically be miles or feet
mrbUnits = arcpy.GetParameterAsText(4)

# Variables for Project tool
# WGS 1984
srWGS84 = arcpy.SpatialReference(4326)
# PA State Plane South (feet) NAD 1983
srSPC = arcpy.SpatialReference(2272)
# Output
outputSPC = r'\\Ccpasr34\psep$\GIS\SARA\SitesLatLong.gdb\InputPoint_SPC_PATTS_{}'.format(pattsID)

try:
    # create point from user entered latitude and longitude
    point = arcpy.Point(lon, lat)
    # create geometry point for use in buffer tool - WGS 1984
    geometryPoint = arcpy.PointGeometry(point, srWGS84)
    # Convert WGS 1984 layer to a NAD 1983 PA State Plane South layer
    arcpy.Project_management(geometryPoint, outputSPC, srSPC, "NAD_1983_To_WGS_1984_1", preserve_shape = "PRESERVE_SHAPE")

    # Multi-ring Buffer tool
    # Output layer
    mrbOutput = r'\\Ccpasr34\psep$\GIS\SARA\RiskRadii.gdb\RiskRadii_PATTS_{}'.format(pattsID)
    # Field name in output layer to store buffer distance
    mrbDistanceField = 'BUFFDIST'
    # Dissolve option
    mrbDissolveOption = 'NONE'
    # Run tool
    arcpy.MultipleRingBuffer_analysis(outputSPC,mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)
    # Add message that Multiple Ring Buffer tool complete
    arcpy.AddMessage('SARA Risk Radii created')
    # Add Field Managment Tool
    # Add field to output layer with buffer distance units
    fieldName = 'UNITS'
    fieldType = 'TEXT'
    fieldExpression = '"{0}"'.format(mrbUnits)
    # Execut Add Field Management tool
    arcpy.AddField_management(mrbOutput, fieldName,fieldType)
    # Add message that Units field added to layer
    arcpy.AddMessage('UNITS field added')
    # Calculate Field Managment Tool
    # Calculate buffer distance units
    arcpy.CalculateField_management(mrbOutput, fieldName, fieldExpression, 'PYTHON_9.3')
    # Add message that buffer distance units added to Units field
    arcpy.AddMessage('The units ' + mrbUnits + ' added to the UNITS field')

except Exception:
        e = sys.exc_info()[1]
        arcpy.AddError(e.args[0])