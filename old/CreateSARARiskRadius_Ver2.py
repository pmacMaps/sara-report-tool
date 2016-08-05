#-------------------------------------------------------------------------------
# Name:        SARA Risk Radius Generator
# Purpose:     Create risk radii for a SARA facility
#              Ver 2 Note: Buffer distance is entered by user
#              Need to validate user input
#              Goal to provide user with drop-down of "miles" or "feet" as options
# Author:      pmckinney
#
# Created:     03/17/2016
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
# Buffer units - will typically be miles or feet
mrbUnits = arcpy.GetParameterAsText(3)
# Field name in output layer to store buffer distance
mrbDistanceField = 'BUFFDIST'
# Dissolve option
mrbDissolveOption = 'NONE'

# Run Multiple Ring Buffer, Add Field, and Calculate field tools
# only if a valid unit is selected for the buffer
try:
    # Execute Multiple Ring Buffer tool
    arcpy.MultipleRingBuffer_analysis(mrbInput,mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)

    # Add message that Multiple Ring Buffer tool complete
    arcpy.AddMessage('SARA Risk Radii created')

    ### Add Field Managment Tool ###
    # Add field to output layer with buffer distance units
    # Set variables
    fieldName = 'UNITS'
    fieldType = 'TEXT'
    fieldExpression = '"{0}"'.format(mrbUnits)

    # Execut tool
    arcpy.AddField_management(mrbOutput, fieldName,fieldType)

    # Add message that Units field added to layer
    arcpy.AddMessage('UNITS field added')

    ### Calculate Field Managment Tool ###
    # Calculate buffer distance units
    arcpy.CalculateField_management(mrbOutput, fieldName, fieldExpression, 'PYTHON_9.3')

    # Add message that buffer distance units added to Units field
    arcpy.AddMessage('The units ' + mrbUnits + ' added to the UNITS field')

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])













