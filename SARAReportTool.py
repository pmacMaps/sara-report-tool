#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        SARA Reporting Tool
#
# Purpose:     To generate risk radii for a SARA facility, estimate the residential population within each risk raidus,
#              and identify vulnerable facilities within each risk radius.
#
# Summary:     User enters the latitude, longitude, and PATTS ID for the SARA facility, risk radius distances and units, and the folder location
#              for the listing of vulnerable facilities in an ArcGIS Desktop tool form.  The tool then runs three analyses: create the risk radii,
#              estimate residential population, and extract vulnerable facilities.  A project map is generated and exported to png
#
# Author:      Patrick McKinney
#
# Created:     08/10/2016
#
# Updated:     05/7/2019
#
# Copyright:   (c) Cumberland County GIS 2019
#
# Disclaimer:  CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THIS TOOL.
#              THE TOOL IS PROVIDED WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
#              OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#              MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#              Furthermore, Cumberland County assumes no liability for any errors,
#              omissions, or inaccuracies in the information provided regardless
#              of the cause of such, or for any decision made, action taken, or action
#              not taken by the user in reliance upon any maps or data provided
#              herein. The user assumes the risk that the information may not be accurate.
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

# import modules
import arcpy, os, riskRadius, populationEstimate, vulnerableFacilities, errorLogger, createMap

try:
    # User entered variables from ArcGIS tool
    # name of SARA facility - string
    sara_name = arcpy.GetParameterAsText(0)
    # address of SARA facility - string
    sara_address = arcpy.GetParameterAsText(1)
    # PATTS ID - string
    patts_id = arcpy.GetParameterAsText(2)
    # latitude of SARA facility - double
    lat = float(arcpy.GetParameterAsText(3))
    # longitude of SARA facility - double
    lon = float(arcpy.GetParameterAsText(4))
    # Buffer distances for risk radii - double, multi-value
    mrb_distances = arcpy.GetParameterAsText(5)
    # Buffer units - string, drop-down list
    mrb_units = arcpy.GetParameterAsText(6)
    # Output directory for analysis reslts - folder
    output_dir = arcpy.GetParameterAsText(7)
    # out file geodatabase nam
    output_gdb_name = 'Analysis_Results_PATTS_{}'.format(patts_id)
    # output file geodatabase
    output_gdb = '{}.gdb'.format(os.path.join(output_dir,output_gdb_name))
    # create a text file in output location
    results_text_file = r'{}\SARA_Analysis_Results_PATTS_{}.txt'.format(output_dir,patts_id)

    # create project file geodatabase
    arcpy.CreateFileGDB_management(output_dir, output_gdb_name, '10.0')
    # add message to user
    arcpy.AddMessage('\nCreated project file geodatabase {} in {}'.format(output_gdb_name, output_dir))

    # Run multiple ring buffer (risk radii)
    sara_site, risk_radii_output = riskRadius.createRiskRadii(lat,lon,patts_id,mrb_distances,mrb_units,output_gdb,results_text_file)

    # Run census popluation estimate tool
    populationEstimate.estimateCensusPopulation(risk_radii_output, patts_id, output_dir, output_gdb, results_text_file)

    # Run vulnerable facilities analysis tool
    vulnerableFacilities.vulnerableFacilitiesAnalysis(risk_radii_output, output_dir)

    # Run map generation tool
    createMap.createSaraMap(sara_site,risk_radii_output,sara_name,sara_address,patts_id,output_dir)
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