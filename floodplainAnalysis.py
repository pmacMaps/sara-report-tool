#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Floodplain Analysis
#
# Ecosystem:   Used in SARAReportTool.py
#
# Purpose:     [update me]
#
# Summary:     [update me]
#
#
#
# Author:      Patrick McKinney
#
# Created:     02/28/2019
#
# Updated:     02/28/2019
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
import arcpy, os, errorLogger

def intersectFloodplainTest(projected_point,lon,lat,results_text_file):
    """Tests whether the building footprint for the SARA site intersects a floodplain"""
    try:
        # file geodatabase on EOC C:
        geodata_gdb = r'C:\GIS\Geodata.gdb'
        # building footprints layer
        blgd_footprints = os.path.join(geodata_gdb, 'Building_Footprints_2008')
        # floodplains
        floodplain_districts = os.path.join(geodata_gdb, 'FEMA_Floodplains_2009')
        # placeholder for contents of text file storing estimate population
        text_file_contents = ''
        # message to write to text file and arcPy info window
        message = ''

        # create feature layers
        arcpy.MakeFeatureLayer_management(blgd_footprints,'Building_Footprints')
        arcpy.MakeFeatureLayer_management(floodplain_districts,'Floodplains')
        arcpy.MakeFeatureLayer_management(projected_point,'SARA_Site')

        # select building footprint that contains SARA Site
        arcpy.SelectLayerByLocation_management('Building_Footprints', 'CONTAINS', 'SARA_Site')
        # get count of selected features
        features_count = int(arcpy.GetCount_management('Building_Footprints')[0])
        # if no features selected, add warning message
        if features_count == 0:
            # add warning message
            arcpy.AddWarning('\nNo Building Footprints contain the SARA Site located at latitude: {}; longitude: {}'.format(lat,lon))
        # if a building footprint is selected, test if it intersects a floodplain
        else:
            arcpy.SelectLayerByLocation_management('Building_Footprints', 'INTERSECT', 'Floodplains', selection_type='SUBSET_SELECTION')
            # get count of selected features
            features_count = int(arcpy.GetCount_management('Building_Footprints')[0])
            # if no features selected, add warning message
            if features_count == 0:
                # add message
                message = 'The building footprint for the SARA Site located at latitude: {}; longitude: {}, does not intersect a floodplain'.format(lat,lon)
                arcpy.AddMessage('\n{}'.format(message))
                text_file_contents += '\n{}\n'.format(message)
            else:
                message = 'The building footprint for the SARA Site located at latitude: {}; longitude: {}, intersects a floodplain'.format(lat,lon)
                arcpy.AddWarning('\n{}'.format(message))
                text_file_contents += '\n{}\n'.format(message)
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
    finally:
         # write message to log file
        try:
            with open(results_text_file, 'a') as f:
                f.write(str(text_file_contents))
        except:
            arcpy.AddError('\nThere was an error writing the floodplain analysis results message to the project text file')