#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Vulnerable Facilities Analysis for Risk Radius
#
# Ecosystem:   Used in SARAReportTool.py
#
# Purpose:     Create an excel spreadsheet of vulnerable facilities located within risk radii.
#              Vulnerable facilities include schools, daycares, medical facilities, assisted living centers, and MHIDD facilities
#
# Summary:     For each record in the SARA risk radii layer, a select by location analysis is run on each vulnerable facility.  The selected features are
#              exported to an excel spreadsheet at a located defined by the user.
#
#              The SARA risk radii layer is created in a previous module wihtin SARAReportTool.py (riskRadius.py)
#
# Author:      Patrick McKinney
#
# Created:     04/28/2016
#
# Updated:     02/21/2019
#
# Copyright:   (c) Cumberland County GIS 2019
#
# Disclaimer:  CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
#              WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#              FITNESS FOR A PARTICULAR PURPOSE.
#              Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
#              of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
#              herein. The user assumes the risk that the information may not be accurate.
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Import modules
import arcpy, os, errorLogger

def vulnerableFacilitiesAnalysis(riskRadius, output_dir):
    """Select vulnerable facilities within risk radius"""

    # function to make feature layer
    def makeFeatureLayer(featureClass,layerName):
        """ Creates a feature layer. Assumes all feature classes within same workspace """
        arcpy.MakeFeatureLayer_management(featureClass,layerName)
    # end makeFeatureLayer

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
    # end function

    try:
        # allow data to be ovewritten
        arcpy.env.overwriteOutput = True
        # file geodatabase containing vulnerable facilities
        arcpy.env.workspace = r'C:\GIS\Geodata.gdb'
        # add message
        arcpy.AddMessage('\nPerforming Vulnerable Facilities analysis\nResults of analysis will be located at {}'.format(outputFolder))
        # create sub-directory to store results of vulnerable facilities anlaysis
        os.mkdir(os.path.join(output_dir, 'Vulnerable Facilities Analysis Results'))
        # add message
        arcpy.AddMessage('Created output directory for Vulnerable Facilities Analysis spreadsheets')
        # output directory for spreadsheets
        output_dir_xls = r'{}\{}'.format(output_dir,'Vulnerable Facilities Analysis Results')

        # Vulnerable Facilities Sites
        # Create Feature Layers for analysis
        # Assisted Living
        makeFeatureLayer('AssistedLiving','Assisted_Living')
        # Daycares
        makeFeatureLayer('Daycare','Daycares')
        # Health Medical Sites
        makeFeatureLayer('HealthMedical','Health_Medical')
        # MHIDD Sites
        makeFeatureLayer('MHIDD_Facility','MHIDD')
        # Schools
        makeFeatureLayer('Education','Schools')

        # make feature layer for risk radii buffer to enable select by attribute
        arcpy.MakeFeatureLayer_management(riskRadius, 'Buffer Layer')

        # fields for cursor
        riskRadiusFields = ['OBJECTID', 'PATTS', 'BUFFDIST', 'UNITS']
        # create search cursor on feature layer
        with arcpy.da.SearchCursor(riskRadius, riskRadiusFields) as cursor:
            for row in cursor:
                # where clause
                whereClause = "OBJECTID = {}".format(row[0])
                # select the current record from the buffer layer using OBJECTID
                # this will set each select by location to be run against the current feature in the buffer layer
                arcpy.SelectLayerByAttribute_management('Buffer Layer', 'NEW_SELECTION', whereClause)
                # Assisted Living
                selectFeaturesExportToExcel('Assisted_Living', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Daycares
                selectFeaturesExportToExcel('Daycares', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Health Medical Sites
                selectFeaturesExportToExcel('Health_Medical', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # MHIDD Sites
                selectFeaturesExportToExcel('MHIDD', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Schools
                selectFeaturesExportToExcel('Schools', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
            # end for
        # end with
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
    # delete cursor
    finally:
        try:
            if cursor:
                del cursor
            else:
                pass
        except:
            pass