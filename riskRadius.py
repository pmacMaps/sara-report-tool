#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Create SARA Risk Radii
#
# Ecosystem:   Used in SARAReportTool.py
#
# Purpose:     Create risk radii (multi-ring buffer) for a user entered SARA facility.
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
# Updated:     03/01/2019
#
# Copyright:   (c) Cumberland County GIS 2019
#
# Disclaimer:  CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
#              WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#              FITNESS FOR A PARTICULAR PURPOSE.
#              Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
#              of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
#              herein. The user assumes the risk that the information may not be accurate.
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

# import modules
import arcpy, os, errorLogger, floodplainAnalysis

def createRiskRadii(lat,lon,patts_id,mrb_distances,mrb_units,out_gbd,text_file):
    """Creates a multi-ring buffer for a SARA facility"""
    try:
        # allow data to be ovewritten
        arcpy.env.overwriteOutput = True
        # Variables for Project tool
        # WGS 1984 geographic coordinate system
        sr_wgs_84 = arcpy.SpatialReference(4326)
        # PA State Plane South (feet) NAD 1983 projected coordinate system
        sr_spc = arcpy.SpatialReference(2272)
        # reprojected point output name
        output_spc_name = 'Input_Point_SPC_PATTS_{}'.format(patts_id)
        # output layer
        output_spc = os.path.join(out_gbd,output_spc_name)

        # create point from user entered latitude and longitude
        point = arcpy.Point(lon, lat)
        # create geometry point for use in buffer tool - WGS 1984
        geometry_point = arcpy.PointGeometry(point, sr_wgs_84)
        # Convert WGS 1984 layer to a NAD 1983 PA State Plane South layer
        arcpy.Project_management(geometry_point, output_spc, sr_spc, "NAD_1983_To_WGS_1984_1", preserve_shape = "PRESERVE_SHAPE")

        # Multi-ring Buffer tool
        # Output layer
        mrb_output = os.path.join(out_gbd, 'RiskRadii_PATTS_{}'.format(patts_id))
        # Field name in output layer to store buffer distance
        mrb_distance_field = 'BUFFDIST'
        # Dissolve option
        mrb_dissolve_option = 'NONE'
        # Run tool
        arcpy.MultipleRingBuffer_analysis(output_spc,mrb_output,mrb_distances,mrb_units,mrb_distance_field,mrb_dissolve_option)
        # Add message that Multiple Ring Buffer tool complete
        arcpy.AddMessage('SARA Risk Radii created for PATTS #{}'.format(patts_id))
        # Add field to output layer with PATTS ID
        field_name_patts = 'PATTS'
        field_type = 'TEXT'
        field_expression_patts = '"{0}"'.format(patts_id)
        # Execut Add Field Management tool
        arcpy.AddField_management(mrb_output,field_name_patts,field_type)
        # Add message that PATTS ID added to layer
        arcpy.AddMessage('PATTS ID field added')
        # Calculate PATTS ID to field
        arcpy.CalculateField_management(mrb_output, field_name_patts, field_expression_patts, 'PYTHON_9.3')
        # Add message that PATTS ID added to PATTS ID field
        arcpy.AddMessage('PATTS ID #{} added to PATTS ID field'.format(patts_id))
        # Add field to output layer with buffer distance units
        field_name_units = 'UNITS'
        field_expression_units = '"{}"'.format(mrb_units)
        # Execut Add Field Management tool
        arcpy.AddField_management(mrb_output,field_name_units,field_type)
        # Add message that Units field added to layer
        arcpy.AddMessage('UNITS field added')
        # Calculate buffer distance units
        arcpy.CalculateField_management(mrb_output, field_name_units, field_expression_units, 'PYTHON_9.3')
        # Add message that buffer distance units added to Units field
        arcpy.AddMessage('The units {} added to the UNITS field'.format(mrb_units))

        # run floodplain analysis module
        floodplainAnalysis.intersectFloodplainTest(output_spc,lon,lat,text_file)

        # make sara risk radii layer available as input to other tools
        return mrb_output
    # If an error occurs running geoprocessing tool(s) capture error and write message
    # handle error outside of Python system
    except EnvironmentError as e:
        arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
        # call error logger method
        errorLogger.PrintException(e)
    # handle exception error
    except Exception as e:
        arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
        # call error logger method
        errorLogger.PrintException(e)