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


# User entered variables from ArcGIS tool
# latitude
lat = arcpy.GetParameterAsText(0)
# longitude
lon = arcpy.GetParameterAsText(1)
# PATTS ID
pattsID = arcpy.GetParameterAsText(2)
# Buffer distances
mrbDistances = arcpy.GetParameterAsText(3)
# Buffer units - will typically be miles or feet
mrbUnits = arcpy.GetParameterAsText(4)
# Output folder for Excel files
outputFolder = arcpy.GetParameterAsText(5)

# Layer Variables
# Regional U.S. Census Blocks - clipping feature
censusBlocks = r'C:\GIS\Geodata.gdb\Regional_Census2010_Blocks_SPS'

# Output Variables
# Output for Geometry Point
outputSPC = r'\\Ccpasr34\psep$\GIS\SARA\SitesLatLong.gdb\InputPoint_SPC_PATTS_{}'.format(pattsID)
# Output for Multi-ring buffer layer - SARA Risk Radii
mrbOutput = r'\\Ccpasr34\psep$\GIS\SARA\RiskRadii.gdb\RiskRadii_PATTS_{}'.format(pattsID)
# Output for Census Population Estimate
outputLocationCensusPop = r'\\ccpasr34\psep$\GIS\SARA\PopEstimates.gdb\\'


# Create Risk Radii Tool

# Variables for Project tool
# WGS 1984
srWGS84 = arcpy.SpatialReference(4326)
# PA State Plane South (feet) NAD 1983
srSPC = arcpy.SpatialReference(2272)

try:
    # create point from user entered latitude and longitude
    point = arcpy.Point(lon, lat)
    # create geometry point for use in buffer tool - WGS 1984
    geometryPoint = arcpy.PointGeometry(point, srWGS84)
    # Convert WGS 1984 layer to a NAD 1983 PA State Plane South layer
    arcpy.Project_management(geometryPoint, outputSPC, srSPC, "NAD_1983_To_WGS_1984_1", preserve_shape = "PRESERVE_SHAPE")

    # Multi-ring Buffer tool
    # Field name in output layer to store buffer distance
    mrbDistanceField = 'BUFFDIST'
    # Dissolve option
    mrbDissolveOption = 'NONE'
    # Run tool
    arcpy.MultipleRingBuffer_analysis(outputSPC,mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)
    # Add message that Multiple Ring Buffer tool complete
    arcpy.AddMessage('SARA Risk Radii created')
    # Add field to output layer with PATTS ID
    fieldNamePatts = 'PATTS'
    fieldType = 'TEXT'
    fieldExpressionPatts = '"{0}"'.format(pattsID)
    # Execut Add Field Management tool
    arcpy.AddField_management(mrbOutput,fieldNamePatts,fieldType)
    # Add message that PATTS ID added to layer
    arcpy.AddMessage('PATTS ID field added')
    # Calculate PATTS ID to field
    arcpy.CalculateField_management(mrbOutput, fieldNamePatts, fieldExpressionPatts, 'PYTHON_9.3')
    # Add message that PATTS ID added to PATTS ID field
    arcpy.AddMessage('PATTS ID added to PATTS ID field')
    # Add field to output layer with buffer distance units
    fieldNameUnits = 'UNITS'
    fieldExpressionUnits = '"{0}"'.format(mrbUnits)
    # Execut Add Field Management tool
    arcpy.AddField_management(mrbOutput, fieldNameUnits,fieldType)
    # Add message that Units field added to layer
    arcpy.AddMessage('UNITS field added')
    # Calculate buffer distance units
    arcpy.CalculateField_management(mrbOutput, fieldNameUnits, fieldExpressionUnits, 'PYTHON_9.3')
    # Add message that buffer distance units added to Units field
    arcpy.AddMessage('The units ' + mrbUnits + ' added to the UNITS field')

    # End Create Risk Radii

    # Estimate Census Population Tool
    # Search cursor for SARA Facility
    cursorCensusPop = arcpy.SearchCursor(mrbOutput)

    fileCountCensusPop = 0
    # Loop through records of SARA Facility
    for row in cursorCensusPop:
        fileCountCensusPop += 1
        # Clip US Census Blocks layer by SARA Facility record
        # Clip feature
        feat = row.Shape
         # PATTS ID
        pattsIDCensusPop = row.PATTS
        # Buffer units
        buffUnits = row.UNITS
        # Buffer distance
        buffDist = str(row.BUFFDIST)
        # Replace . with _ in buffer distance
        buffDistReplace = buffDist.replace('.', '_')
        # Buffer units and distance
        buffAppend = '{}_{}'.format(buffDistReplace, buffUnits)
        # Output appended text for clip
        outputCensusPopAppend = 'EstCensusPop_PATTS_{}_{}_{}'.format(pattsIDCensusPop, buffAppend, fileCount)
        # Boiler place text for ArcPy message
        messageTextCensusPop = 'PATTS {} risk radius {}-{}'.format(pattsIDCensusPop, buffDist, buffUnits)
        # Execute Clip tool
        censusBlocksClip = arcpy.Clip_analysis(censusBlocks, feat, outputLocationCensusPop + outputAppend)
        # Add message that Clip is completed
        arcpy.AddMessage('Census Blocks clipped for ' + messageTextCensusPop)
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
        arcpy.AddMessage('Table of total estimated population created for PATTS {} risk radius {}-{}'.format(pattsID, buffDist, buffUnits))
    del cursor, row

except Exception:
        e = sys.exc_info()[1]
        arcpy.AddError(e.args[0])