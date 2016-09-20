#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        SARA Tier 2 Reporting Tool
#
# Purpose:     To generate risk radii for a SARA facility, estimate the residential population within each risk raidus,
#              and identify vulnerable facilities within each risk radius.
#
# Summary:     User enters the latitude, longitude, and PATTS ID for the SARA facility, risk radius distances and units, and the folder location
#              for the listing of vulnerable facilities in an ArcGIS Desktop geoprocessing tool form.  The tool then runs three analyses: create the risk radii,
#              estimate residential population, and extract vulnerable facilities.#
#
# Author:      Patrick McKinney
# Created:     08/10/2016
#
# Updated:     09/20/2016
#
# Copyright:   (c) Cumberland County GIS 2016
#
# Disclaimer:  CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
#              WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#              FITNESS FOR A PARTICULAR PURPOSE.
#              Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
#              of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
#              herein. The user assumes the risk that the information may not be accurate.
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

# access ArcPy module
import arcpy

# Import component tools
import riskRadius, populationEstimate, vulnerableFacilities

# User entered variables from ArcGIS tool
# latitude
# For ArcMap tool, this input is required and is a Double format
lat = float(arcpy.GetParameterAsText(0))
# longitude
# For ArcMap tool, this input is required and is a Double format
lon = float(arcpy.GetParameterAsText(1))
# PATTS ID
# For ArcMap tool, this input is required and is a String format
pattsID = arcpy.GetParameterAsText(2)
# Buffer distances
# For ArcMap tool, this input is required and is a Double format.  Multiple inputs are allowed.
mrbDistances = arcpy.GetParameterAsText(3)
# Buffer units - will typically be miles or feet
# For ArcMap tool, this input is required and is a String format
mrbUnits = arcpy.GetParameterAsText(4)
# Output folder for Excel files
# For ArcMap tool, this input is required and is a Folder format
outputFolder = arcpy.GetParameterAsText(5)

# Run multiple ring buffer (risk radii)
# This function converts the latitude and longitude entered in the ArcGIS tool from WGS 1984 to another projected coordinate system defined in riskRadius.py.
# It then performs a multi-ring buffer on this point feature using the buffer distances and units entered in the ArcGIS tool.
# The function returns the multi-ring buffer layer, which is used as an input for other functions in this script.
mrbOutput = riskRadius.createRiskRadii(lat,lon,pattsID,mrbDistances,mrbUnits)

# Run census popluation estimate tool
# This function clips Census data to each feature in the multi-ring buffer layer created in the riskRadius.createRiskRadii() function.
# A proportional population value is calculated by creating a ratio of the clipped area to original area and multiplying that by the popluation for the Census geography.
# A table is also created that sums the total proportional population.
populationEstimate.estimateCensusPopulation(mrbOutput)

# Run vulnerable facilities analysis tool
# This function performs a select by location analysis for each vulnerable facility for each feature (record) in the multi-ring buffer layer created in the
# riskRadius.createRiskRadii() function.  If there are vulnerable facilities that interesct the buffer, the selected features are exported to an
# Excel spreadsheet.
vulnerableFacilities.vulnerableFacilitiesAnalysis(mrbOutput, outputFolder)