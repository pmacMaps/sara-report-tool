#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Create SARA Risk Radii
#
# Ecosystem:   Used in SARAReportTool.py
#
# Purpose:     Create risk radii for a user entered SARA facility.
#
# Summary:     Latitude, longitude, PATTS ID, risk-radius distances, and risk radius units
#              are entered in the ArcGIS tool run from SARAReportTool.py
#
#              A geometry point is created from latitude and longitude and converted to PA State Plane South (ft) (SPC).
#              The multi-ring buffer tool is run on the SPC point using the risk-radius distances and units.
#
# Author:      Patrick McKinney
#
# Created:     07/26/2016
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

# import modules
import arcpy, sys

def createRiskRadii(lat,lon,pattsID,mrbDistances,mrbUnits):
    """Creates a multi-ring buffer for a SARA facility"""

    # allow data to be ovewritten
    arcpy.env.overwriteOutput = True

    # Variables for Project tool
    # WGS 1984
    srWGS84 = arcpy.SpatialReference(4326)
    # PA State Plane South (feet) NAD 1983
    srSPC = arcpy.SpatialReference(2272)
    # Output
    outputSPC = r'\\Ccpasr34\psep$\GIS\SARA\SitesLatLong.gdb\InputPoint_SPC_PATTS_{}'.format(pattsID)

    try:
        # create point from user entered latitude and longitude
        point = arcpy.Point(lon, lat)
        # create geometry point for use in buffer tool - WGS 1984
        geometryPoint = arcpy.PointGeometry(point, srWGS84)
        # Convert WGS 1984 layer to a NAD 1983 PA State Plane South layer
        arcpy.Project_management(geometryPoint, outputSPC, srSPC, "NAD_1983_To_WGS_1984_1", preserve_shape = "PRESERVE_SHAPE")

        # Multi-ring Buffer tool
        # Output layer
        mrbOutput = r'\\Ccpasr34\psep$\GIS\SARA\RiskRadii.gdb\RiskRadii_PATTS_{0}'.format(pattsID)
        # Field name in output layer to store buffer distance
        mrbDistanceField = 'BUFFDIST'
        # Dissolve option
        mrbDissolveOption = 'NONE'
        # Run tool
        arcpy.MultipleRingBuffer_analysis(outputSPC,mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)
        # Add message that Multiple Ring Buffer tool complete
        arcpy.AddMessage('SARA Risk Radii created for PATTS #{0}'.format(pattsID))
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
        arcpy.AddMessage('PATTS ID #{} added to PATTS ID field'.format(pattsID))
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
        arcpy.AddMessage('The units {0} added to the UNITS field'.format(mrbUnits))

        # make sara risk radii layer available as input to other tools
        return mrbOutput

    # If an error occurs running geoprocessing tool(s) capture error and write message
    # handle error outside of Python system
    except EnvironmentError as e:
        arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
        # Store information about the error
        tbE = sys.exc_info()[2]
        # add the line number the error occured to the log message
        arcpy.AddError('\nTool failed at Line {0} in {1}'.format(tbE.tb_lineno, sys.argv[0]))
        # add the error message to the log message
        arcpy.AddError('\nError: {0}'.format(str(e)))
    # handle exception error
    except Exception as e:
        arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
        # Store information about the error
        tbE = sys.exc_info()[2]
        # add the line number the error occured to the log message
        arcpy.AddError('Tool failed at Line {0} in {1}'.format(tbE.tb_lineno, sys.argv[0]))
        # add the error message to the log message
        arcpy.AddError('\nError: {0}'.format(e.message))