#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        SARA Reporting Tool
#
# Purpose:     To generate risk radii for a SARA facility, estimate the residential population within each risk raidus,
#              and identify vulnerable facilities within each risk radius.
#
# Summary:     User enters the latitude, longitude, and PATTS ID for the SARA facility, risk radius distances and units, and the folder location
#              for the listing of vulnerable facilities in an ArcGIS Desktop tool form.  The tool then runs three analyses: create the risk radii,
#              estimate residential population, and extract vulnerable facilities.#
#
# Author:      Patrick McKinney
# Created:     08/10/2016
#
# Updated:     02/14/2019
#
# Copyright:   (c) Cumberland County GIS 2019
#
# Disclaimer:  CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
#              WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#              FITNESS FOR A PARTICULAR PURPOSE.
#              Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
#              of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
#              herein. The user assumes the risk that the information may not be accurate.
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

# import modules
import arcpy, os, riskRadius, populationEstimate, vulnerableFacilities

try:
    # User entered variables from ArcGIS tool
    # latitude
    lat = float(arcpy.GetParameterAsText(0))
    # longitude
    lon = float(arcpy.GetParameterAsText(1))
    # PATTS ID
    patts_id = arcpy.GetParameterAsText(2)
    # Buffer distances
    mrb_distances = arcpy.GetParameterAsText(3)
    # Buffer units - will typically be miles or feet
    mrb_units = arcpy.GetParameterAsText(4)
    # Output directory for analysis reslts
    output_dir = arcpy.GetParameterAsText(5)
    # out file geodatabase nam
    output_gdb_name = 'Analysis_Results_PATTS_{}'.format(patts_id)
    # output file geodatabase
    output_gdb = os.path.join(output_dir,output_gdb_name)

    # create project file geodatabase
    arcpy.CreateFileGDB_management(output_dir, output_gdb_name, '10.0')
    # add message to user
    arcpy.AddMessage('\nCreated project file geodatabase {} in {}\n'.format(output_gdb_name, output_dir))

    # Run multiple ring buffer (risk radii)
    risk_radii_output = riskRadius.createRiskRadii(lat,lon,patts_id,mrb_distances,mrb_units,output_gdb)

    # Run census popluation estimate tool
    populationEstimate.estimateCensusPopulation(risk_radii_output, patts_id, output_dir, output_gdb)

    # Run vulnerable facilities analysis tool
    vulnerableFacilities.vulnerableFacilitiesAnalysis(risk_radii_output, output_dir)
except:
    pass