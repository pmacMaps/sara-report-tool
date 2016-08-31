#----------------------------------------------------------------------------------------------#
# Name:        SARA Reporting Tool
#
# Purpose:     []
#
# Summary:     []
#
#
# Author:      Patrick McKinney
# Created:     08/10/2016
# Updated:
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#----------------------------------------------------------------------------------------------#

# access ArcPy module
import arcpy

# Import Create Risk Radius Tool
import CreateSARARiskRadius


# User entered variables from ArcGIS tool
# latitude
lat = float(arcpy.GetParameterAsText(0))
# longitude
lon = float(arcpy.GetParameterAsText(1))
# PATTS ID
pattsID = arcpy.GetParameterAsText(2)
# Buffer distances
mrbDistances = arcpy.GetParameterAsText(3)
# Buffer units - will typically be miles or feet
mrbUnits = arcpy.GetParameterAsText(4)
# Output folder for Excel files
outputFolder = arcpy.GetParameterAsText(5)

mrbOutput = CreateSARARiskRadius.createRiskRadii(lat,lon,pattsID,mrbDistances,mrbUnits)
