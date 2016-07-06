#-------------------------------------------------------------------------------------------
# Name:        Create SARA Risk Radii
# Purpose:     Create risk radii for a user selected SARA facility
#              User enters the PATTS ID for the facility, buffer distances, and buffer units.
#              The script checks to see if the input PATTS ID exists in the SARA layer.
#              If so, the script runs a multi-ring buffer within a try/except block.
# Author:      Patrick McKinney#
# Created:     03/17/2016
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------------------

# Import arcpy
import arcpy

# SARA layer
sara = r'C:\GIS\Geodata.gdb\SARA'
# PATTS ID field for SARA
saraPATTSField = 'PATTS'
# User selected SARA site by PATTS ID
# PATTS ID is an integer field in dataset
pattsID = int(arcpy.GetParameterAsText(0))
# String version of pattsID
pattsIDString = str(pattsID)
# List holding PATTS IDs of SARA sites
saraList = []

# Create a cursor to search the PATTS ID field of SARA
cur = arcpy.SearchCursor(sara, "", "", saraPATTSField)
# Add SARA PATTS IDs to list
for row in cur:
    saraList.append(row.PATTS)
del cur, row

# Check if user entered PATTS ID exists in SARA layer
if pattsID in saraList:
    # SQL statement to apply definition query to SARA layer
    whereClause = "{} = {}".format(arcpy.AddFieldDelimiters(sara,saraPATTSField), pattsID)
    # Create in-memory layer of SARA with selected site
    arcpy.MakeFeatureLayer_management(sara, "mrbInput", whereClause)
    # Output layer
    mrbOutput = r'\\Ccpasr34\psep$\GIS\SARA\RiskRadii.gdb\RiskRadii_PATTS_{}'.format(pattsIDString)
    # Buffer distances
    mrbDistances = arcpy.GetParameterAsText(1)
    # Buffer units - will typically be miles or feet
    mrbUnits = arcpy.GetParameterAsText(2)
    # Field name in output layer to store buffer distance
    mrbDistanceField = 'BUFFDIST'
    # Dissolve option
    mrbDissolveOption = 'NONE'
    # Run Multiple Ring Buffer, Add Field, and Calculate field tools
    # only if a valid unit is selected for the buffer
    try:
        # Execute Multiple Ring Buffer tool
        arcpy.MultipleRingBuffer_analysis("mrbInput",mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)
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
else:
    # Add message that invalid PATTS ID entered
    arcpy.AddError('The SARA facility you entered is not in the database.')