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
# Updated:     05/13/2019
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
import arcpy, os, errorLogger, exportLayersToExcel

# function to make feature layer
def makeFeatureLayer(featureClass,layerName, clause=""):
   """ Creates a feature layer. Assumes all feature classes within same workspace """
   arcpy.MakeFeatureLayer_management(featureClass,layerName, where_clause=clause)

def vulnerableFacilitiesAnalysis(riskRadius, output_dir):
    """Select vulnerable facilities within risk radius"""
    try:
        # allow data to be ovewritten
        arcpy.env.overwriteOutput = True
        # file geodatabase containing vulnerable facilities
        arcpy.env.workspace = r'C:\GIS\Geodata.gdb'
        # add message
        arcpy.AddMessage('\nPerforming Vulnerable Facilities analysis\nResults of analysis will be located at {}'.format(output_dir))
        # create sub-directory to store results of vulnerable facilities anlaysis
        os.mkdir(os.path.join(output_dir, 'Vulnerable Facilities Analysis Results'))
        # output directory for spreadsheets
        output_dir_xls = r'{}\{}'.format(output_dir,'Vulnerable Facilities Analysis Results')
        # Vulnerable Facilities Sites
        # Create Feature Layers for analysis
        # Assisted Living
        makeFeatureLayer('EOC_AssistedLiving','Assisted_Living')
        # Daycares
        makeFeatureLayer('EOC_Daycare','Daycares')
        # Health Medical Sites
        makeFeatureLayer('Site_HealthMedical','Health_Medical', """FCode <> 80026""")
        # MHIDD Sites
        makeFeatureLayer('EOC_MHIDD_Facility','MHIDD')
        # Schools
        makeFeatureLayer('Site_Education','Schools')
        # SARA Facilities
        makeFeatureLayer('EOC_SARA', 'SARA')
        # Hydrography (NHD)
        makeFeatureLayer('NHD_Streams', 'Streams')
        # Municipalities
        makeFeatureLayer('Pennsylvania_Municipalities', 'Municipality')
        # Counties
        makeFeatureLayer('Pennsylvania_Counties', 'County')
        # Water Filtration Plants
        # makeFeatureLayer('', 'Water_Plants')
        # Natural Gas Facilities
        makeFeatureLayer('NPMS_Pipelines', 'Natural_Gas')

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
                exportLayersToExcel.selectFeaturesExportToExcel('Assisted_Living', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Daycares
                exportLayersToExcel.selectFeaturesExportToExcel('Daycares', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Health Medical Sites
                exportLayersToExcel.selectFeaturesExportToExcel('Health_Medical', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # MHIDD Sites
                exportLayersToExcel.selectFeaturesExportToExcel('MHIDD', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Schools
                exportLayersToExcel.selectFeaturesExportToExcel('Schools', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # SARA
                exportLayersToExcel.selectFeaturesExportToExcel('SARA', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Hydrography
                exportLayersToExcel.selectFeaturesExportToExcel('Streams', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Municipalities
                exportLayersToExcel.selectFeaturesExportToExcel('Municipality', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Counties
                exportLayersToExcel.selectFeaturesExportToExcel('County', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Water Filtration Plants
                # selectFeaturesExportToExcel('Water_Plants', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
                # Natural Gas Facilities
                exportLayersToExcel.selectFeaturesExportToExcel('Natural_Gas', 'Buffer Layer', row[2], row[3], row[1], output_dir_xls)
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