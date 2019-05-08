#-------------------------------------------------------------------------------
# Name:        Export Layer as Excel File
#
# Purpose:     Exports selected features from layer to Excel.  Adds warning message if no features selected
#
# Author:      Patrick McKinney
#
# Created:     4/12/2019
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
#-------------------------------------------------------------------------------

import arcpy, os

# function to select layers by location and export selected features to an excel spreadsheet
def selectFeaturesExportToExcel(featureLayer, intersectLayer, bufDist, bufUnits, patts, outLocation):
    """ function to select layers by location and export selected features to an excel spreadsheet
        featureLayer = the feature layer to select records from
        intersectLayer = the layer to select the featureLayer against
        bufDist = the field in the intersectLayer containing the buffer distances
        bufUnits = the field in the intersectLayer containing the buffer units
        patts = PATTS ID for SARA site
        outLocation = the folder that output datasets are placed in.  This is a user parameter in  the tools' form
    """
    # select layer by location - intersect
    arcpy.SelectLayerByLocation_management(featureLayer, 'INTERSECT', intersectLayer)
    # get count of selected features
    featuresCount = int(arcpy.GetCount_management(featureLayer)[0])
    # if no features selected, add warning message
    if featuresCount == 0:
       # add warning message
       arcpy.AddWarning('\nNo features from {} intersect the {}-{} buffer'.format(featureLayer,bufDist,bufUnits))
    # if features are selected, export them to excel file
    else:
       # name for excel file
       fileName = '{} Intersect {} {} {} Buffer.xls'.format(featureLayer,patts,bufDist,bufUnits)
       # output file
       outFile = os.path.join(outLocation,fileName)
       # export to excel
       arcpy.TableToExcel_conversion(featureLayer,outFile)
       # add message
       arcpy.AddMessage('\nExported features from {} layer that intersect the {}-{} buffer to a Microsoft Excel file'.format(featureLayer, bufDist, bufUnits))
   # end if/else