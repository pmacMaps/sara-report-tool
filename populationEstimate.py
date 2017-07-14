#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Estimate Census Population for Risk Radius
#
# Ecosystem:   Used in SARAReportTool.py
#
# Purpose:     Create resident population estimates for each risk radius of a SARA facility
#
# Summary:     For each record in the SARA risk radii layer, the 2010  U.S. Census block dataset is clipped to the risk radius.  A proportional
#              residential population is calculated based upon how much of the block is within the risk radius.  A table is generated that calculates
#              the total proportional population within the risk radius.
#
#              The SARA risk radii layer is created in the previous module wihtin SARAReportTool.py (riskRadius.py)
#
# Author:      Patrick McKinney
#
# Created:     03/16/2016
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
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# Import modules
import arcpy, sys

def estimateCensusPopulation(riskRadius):
    """Calculate estimated population within each risk radius"""

    # allow data to be overwritten
    arcpy.env.overwriteOutput = True

    # Regional U.S. Census Blocks - clipping feature
    censusBlocks = r'C:\GIS\Geodata.gdb\Regional_Census2010_Blocks_SPS'

    # Search cursor for SARA Facility Risk Radii
    cursor = arcpy.SearchCursor(riskRadius)
    try:
        fileCount = 0
        # Loop through records of SARA Facility
        for row in cursor:
            fileCount += 1
            # Clip US Census Blocks layer by SARA Facility record
            # Clip feature
            feat = row.Shape
             # PATTS ID
            pattsID = row.PATTS
            # Buffer units
            buffUnits = row.UNITS
            # Buffer distance
            buffDist = str(row.BUFFDIST)
            # Replace . with _ in buffer distance
            buffDistReplace = buffDist.replace('.', '_')
            # Buffer units and distance
            buffAppend = '{0}_{1}'.format(buffDistReplace, buffUnits)
            # Output
            outputLocation = r'\\ccpasr34\psep$\GIS\SARA\PopEstimates.gdb\\'
            # Output appended text for clip
            outputAppend = 'EstCensusPop_PATTS_{0}_{1}_{2}'.format(pattsID, buffAppend, fileCount)
            # Boiler place text for ArcPy message
            messageText = 'PATTS {0} risk radius {1}-{2}'.format(pattsID, buffDist, buffUnits)
            # Execute Clip tool
            newInput = arcpy.Clip_analysis(censusBlocks, feat, outputLocation + outputAppend)
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
            outTable = outputLocation + outputAppend + '_SumPop'
            statsFields = [['ESTPOP', 'SUM']]
            arcpy.Statistics_analysis(newInput, outTable, statsFields)
            # Add message that estimated population sum table created
            arcpy.AddMessage('Table of total estimated population created for PATTS {0} risk radius {1}-{2}'.format(pattsID, buffDist, buffUnits))
        del cursor, row
    except Exception:
        e = sys.exc_info()[1]
        arcpy.AddError(e.args[0])