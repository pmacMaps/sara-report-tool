#----------------------------------------------------------------------------------------------------#
# Name:        Estimate Census Population for Risk Radius
#
# Purpose:     Create resident population estimates for each risk radius of a SARA facility
#
# Summary:     User selects a SARA risk radius layer.  For each record in that layer, the
#              2010  U.S. Census block dataset is clipped to the risk radius.  A proportional
#              resident population is calculated based upon how much of the block is within the
#              risk radius.  A table is generated that calculates the total proportional population
#              within the risk radius

# Author:      Patrick McKinney#
# Created:     03/16/2016
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#---------------------------------------------------------------------------------------------------#

# Import arcpy
import arcpy

# SARA Facility - feature to be clipped
sara = arcpy.GetParameterAsText(0)
# Regional U.S. Census Blocks - clipping feature
censusBlocks = r'C:\GIS\Geodata.gdb\SARA\Regional_Census2010_Blocks_SPS'
# Output of Clip Operation
#output = arcpy.GetParameterAsText(1)

# Search cursor for SARA Facility
cursor = arcpy.SearchCursor(sara)
try:
    # Loop through records of SARA Facility
    for row in cursor:
        # Clip US Census Blocks layer by SARA Facility record
        # Clip feature
        feat = row.Shape
        # PATTS ID
        pattsID = str(row.PATTS)
        # Buffer units
        buffUnits = row.UNITS
        # Buffer distance
        buffDist = str(int(row.BUFFDIST))
        # Buffer units and distance
        buffAppend = '_{}_{}'.format(buffUnits, buffDist)
        # Output
        output = r'\\ccpasr34\psep$\GIS\SARA\PopEstimates.gdb'
        # Output appended text for clip
        outputAppend = 'EstCensusPop_{}_{}'.format(pattsID, buffAppend)
        # Boiler place text for ArcPy message
        messageText = 'PATTS {} {}-{} risk radius'.format(pattsID,patbuffDist, buffUnits)
        # Execute Clip tool
        newInput = arcpy.Clip_analysis(censusBlocks, feat, output + outputAppend)
        # Add message that Clip is completed
        arcpy.AddMessage('Census Blocks clipped for ' + messageText)
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
        # Calculate the new area to old area ratio for each Census Block
        areaRatioFieldExpression = '!Shape_Area! / !ORAREA!'
        arcpy.CalculateField_management(newInput, 'AREARATIO', areaRatioFieldExpression, 'PYTHON_9.3')
        # Add message that Area Ratio has been calculated
        arcpy.AddMessage('New area to original area ratio calculated for ' + messageText)
        # Calculate the estimated population in each census block based upon the area ratio
        estimatedPopulationFieldExpression = '!POP10! * !AREARATIO!'
        arcpy.CalculateField_management(newInput, 'ESTPOP', estimatedPopulationFieldExpression, 'PYTHON_9.3')
        # Add message that Estimated Population has been calculated
        arcpy.AddMessage('Estimated population calculated for ' + messageText)
        # Calculate the total assumed population and export to dBASE table
        outTable = output + outputAppend + '_SumPop'
        statsFields = [['ESTPOP', 'SUM']]
        arcpy.Statistics_analysis(newInput, outTable, statsFields)
        # Add message that estimated population sum table created
        arcpy.AddMessage('Table of total estimated population created for ' + buffDist + '-' + buffUnits + ' risk radius')
    del cursor, row
except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])