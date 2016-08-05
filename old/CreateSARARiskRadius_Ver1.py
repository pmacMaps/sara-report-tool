#-------------------------------------------------------------------------------
# Name:        SARA Risk Radius Generator
# Purpose:     Create risk radii for a SARA facility
#              Ver 1 Note: Assumes buffer distance will always be in miles
# Author:      pmckinney
#
# Created:     03/16/2016
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import arcpy
import arcpy

### Multiple Ring Buffer Tool ###
# Set variables
# Input layer
mrbInput = arcpy.GetParameterAsText(0)
# Output layer
mrbOutput = arcpy.GetParameterAsText(1)
# Buffer distances
mrbDistances = arcpy.GetParameterAsText(2)
# Buffer units
mrbUnits = 'miles' # or should user select this from options?
# Field name in output layer to store buffer distance
mrbDistanceField = 'BUFFDIST'
# Dissolve option
mrbDissolveOption = 'NONE'

# Execute tool
arcpy.MultipleRingBuffer_analysis(mrbInput,mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)






