#-------------------------------------------------------------------------------
# Name:        Estimate Census Population for Risk Radius
# Purpose:     Create resident population estimates for each risk radius of a
#              SARA facility
#
# Author:      pmckinney
#
# Created:     03/16/2016
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import arcpy
import arcpy

# Variables for Clip tool
# SARA Facility
sara = arcpy.GetParameterAsText(0)
# Clip Feature - Regional U.S. Census Blocks
censusBlocks = r'\\CCPASR07\ncgs$\Scripts\ArcGIS Geoprocessing\SARA Tool\SARA_Tool_DEV.gdb\Regional_Census2010_Blocks_SPS'
# Output
output = arcpy.GetParameterAsText(1)

# Search cursor for SARA Facility
#cursor = arcpy.da.SearchCursor(sara, ['Shape', 'UNITS', 'BUFFDIST'])
cursor = arcpy.SearchCursor(sara) # old cursor syntax

try:
    # Loop through records of SARA Facility
    for row in cursor:
        # Clip US Census Blocks layer by SARA Facility record

        # Clip feature
        feat = row.Shape
        #feat = row[0]

        # Append buffer units and distances to output name
        # Buffer units
        buffUnits = row.UNITS
        #buffUnits = row[1]
        # Buffer distance
        buffDist = str(int(row.BUFFDIST))
        #buffDist = str(int(row[2]))
        # Buffer units and distance
        buffAppend = '_' + buffUnits + '_' + buffDist
        # Boiler place text for ArcPy message
        messageText = buffDist + '-' + buffUnits + ' risk radius'

        # Execute Clip tool
        newInput = arcpy.Clip_analysis(censusBlocks, feat, output + buffAppend)

        # Add message that Clip is completed
        arcpy.AddMessage('Census Blocks clipped for ' + messageText)

        # Add fields to hold results of field calculations

        # Add field to hold clip area to original area ratio
        areaRatioFieldName = 'AREARATIO'
        areaRatioFieldType = 'DOUBLE'

        # Execut Add Field tool
        arcpy.AddField_management(newInput, areaRatioFieldName, areaRatioFieldType)

        # Add message that Area Ratio Field has been added
        arcpy.AddMessage('Area Ratio field added for ' + messageText)

        # Add field to hold estimated population
        estPopFieldName = 'ESTPOP'
        estPopFieldType = 'LONG'

        # Execut Add Field tool
        arcpy.AddField_management(newInput, estPopFieldName, estPopFieldType)

        # Add message that Estimated Population Field has been added
        arcpy.AddMessage('Estimated Population field added for ' + messageText)

        # Delete this after confirming it is not used
        #areaInField = arcpy.ListFields(newInput, 'AREARATIO')[0]
        #newArea = arcpy.ListFields(newInput, 'Shape_Area')[0]
        #orgArea = arcpy.ListFields(newInput, 'ORAREA')[0]

        # areaInField = newInput.AREARATIO
        # orgArea = newInput.ORAREA
        #newArea = row.Shape_Area
        #fieldExpression = '{0} / {1}'.format(newArea, orgArea)
        #fieldExpression = newArea / orgArea
        #arcpy.CalculateField_management(newInput, areaInField, fieldExpression, 'PYTHON_9.3')

        # Calculate the new area to old area ratio for each Census Block
        areaRatioFieldExpression = '!Shape_Area! / !ORAREA!'
        arcpy.CalculateField_management(newInput, 'AREARATIO', areaRatioFieldExpression, 'PYTHON_9.3')

        # Add message that Area Ratio has been calculated
        arcpy.AddMessage('New area to original area ratio calculated for ' + messageText)

        # Calculate the estimated population in each census block
        # based upon the area ratio
        estimatedPopulationFieldExpression = '!POP10! * !AREARATIO!'
        arcpy.CalculateField_management(newInput, 'ESTPOP', estimatedPopulationFieldExpression, 'PYTHON_9.3')

        # Add message that Estimated Population has been calculated
        arcpy.AddMessage('Estimated population calculated for ' + messageText)

        # Calculate the total assumed population and export to dBASE table
    ##    arcpy.env.workspace = r'\\CCPASR07\ncgs$\Scripts\ArcGIS Geoprocessing\SARA Tool\SARA_Tool_DEV.gdb'
        #outTableName = output + buffAppend + '_SumPop'
        outTable = output + buffAppend + '_SumPop'
        statsFields = [['ESTPOP', 'SUM']]
        arcpy.Statistics_analysis(newInput, outTable, statsFields)

        # Add message that estimated population sum table create
        arcpy.AddMessage('Table of total estimated population created for ' + buffDist + '-' + buffUnits + ' risk radius')

    del cursor, row

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])