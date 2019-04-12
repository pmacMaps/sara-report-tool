#-------------------------------------------------------------------------------
# Name:        Export Layer as Excel
#
# Purpose:     Exports selected features from layer to Excel.  Adds warning message if no features selected
#
# Author:      pmckinney
#
# Created:     4/12/2019
# Copyright:   Cumberland County 2019
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