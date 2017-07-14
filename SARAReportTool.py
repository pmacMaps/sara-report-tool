#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        SARA Reporting Tool
#
# Purpose:     To generate risk radii for a SARA facility, estimate the residential population within each risk raidus,
#              and identify vulnerable facilities within each risk radius.
#
# Summary:     User enters the latitude, longitude, and PATTS ID for the SARA facility, risk radius distances and units, and the folder location
#              for the listing of vulnerable facilities in an ArcGIS Desktop tool form.  The tool then runs three analyses: create the risk radii,
#              estimate residential population, and extract vulnerable facilities.#
#
# Author:      Patrick McKinney
# Created:     08/10/2016
#
# Updated:     07/14/2017
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

# import modules
import arcpy, riskRadius, populationEstimate, vulnerableFacilities

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

# Run multiple ring buffer (risk radii)
mrbOutput = riskRadius.createRiskRadii(lat,lon,pattsID,mrbDistances,mrbUnits)

# Run census popluation estimate tool
populationEstimate.estimateCensusPopulation(mrbOutput)

# Run vulnerable facilities analysis tool
vulnerableFacilities.vulnerableFacilitiesAnalysis(mrbOutput, outputFolder)