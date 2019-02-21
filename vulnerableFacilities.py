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
import arcpy, sys, os

def vulnerableFacilitiesAnalysis(riskRadius, output_dir):
    try:
        """Select vulnerable facilities within risk radius"""
        # allow data to be ovewritten
        arcpy.env.overwriteOutput = True
        # Vulnerable Facilities Sites
        # Create Feature Layers for analysis
        # file geodatabase containing vulnerable facilities
        arcpy.env.workspace = r'C:\GIS\Geodata.gdb'
        # Assisted Living
        assistedLiving = 'AssistedLiving'
        arcpy.MakeFeatureLayer_management(assistedLiving, 'assistedLiving_lyr')
        # Daycares
        daycares = 'Daycare'
        arcpy.MakeFeatureLayer_management(daycares, 'daycares_lyr')
        # Health Medical Sites
        medical = 'HealthMedical'
        arcpy.MakeFeatureLayer_management(medical, 'medical_lyr')
        # MHIDD Sites
        mhIdd = 'MHIDD_Facility'
        arcpy.MakeFeatureLayer_management(mhIdd, 'mhIdd_lyr')
        # Schools
        schools = 'Education'
        arcpy.MakeFeatureLayer_management(schools, 'schools_lyr')

         # fields for risk radius layer
        riskRadiusFields = ['Shape', 'PATTS', 'BUFFDIST', 'UNITS']
        # Search cursor for SARA Facility Risk Radii
        with arcpy.da.SearchCursor(riskRadius, riskRadiusFields) as cursor:
            for row in cursor:
             # Replace . with _ in buffer distance
             buffer_distance_replace = str(row[2]).replace('.', '_')
            # Assisted Living
            # Select Assisted Living sites that intersect SARA risk radius
            arcpy.SelectLayerByLocation_management('assistedLiving_lyr', 'INTERSECT', riskRadius, "", 'NEW_SELECTION')
            # Test if any features are selected
            matchCountAL = int(arcpy.GetCount_management('assistedLiving_lyr')[0])
            # If no features selected, add message indicating no features selected
            if matchCountAL == 0:
                arcpy.AddMessage('No Assisted Living Facilities located within within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            else:
                # If features selected, export selected features to Excel
                arcpy.TableToExcel_conversion('assistedLiving_lyr', outputFolder + r'\AssistedLiving_PATTS_{0}_{1}_{2}_{3}.xls'.format(pattsID, buffDistReplace, buffUnits, fileCount))
                # Add status message to ArcGIS dialog box
                arcpy.AddMessage('Completed extracting to Excel the Assisted Living Facilities within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            # Daycares
            # Select Daycares sites that intersect SARA risk radius
            arcpy.SelectLayerByLocation_management('daycares_lyr', 'INTERSECT', riskRadius, "", 'NEW_SELECTION')
            matchCountDaycares = int(arcpy.GetCount_management('daycares_lyr')[0])
            # If no features selected, add message indicating no features selected
            if matchCountDaycares == 0:
                arcpy.AddMessage('No Daycares located within within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            else:
                # If features selected, export selected features to Excel
                arcpy.TableToExcel_conversion('daycares_lyr', outputFolder + r'\Daycares_PATTS_{0}_{1}_{2}_{3}.xls'.format(pattsID, buffDistReplace, buffUnits, fileCount))
                # Add status message to ArcGIS dialog box
                arcpy.AddMessage('Completed extracting to Excel the Daycares within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            # Health Medical
            # Select Health Medical sites that intersect SARA risk radius
            arcpy.SelectLayerByLocation_management('medical_lyr', 'INTERSECT', riskRadius, "", 'NEW_SELECTION')
            # Test if any features are selected
            matchCountMH = int(arcpy.GetCount_management('medical_lyr')[0])
            # If no features selected, add message indicating no features selected
            if matchCountMH == 0:
                arcpy.AddMessage('No Medical Facilities located within within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            else:
                # If features selected, export selected features to Excel
                arcpy.TableToExcel_conversion('medical_lyr', outputFolder + r'\MedicalSites_PATTS_{0}_{1}_{2}_{3}.xls'.format(pattsID, buffDistReplace, buffUnits, fileCount))
                # Add status message to ArcGIS dialog box
                arcpy.AddMessage('Completed extracting to Excel the Medical Facilities within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            # MHIDD
            # Select MHIDD sites that intersect SARA risk radius
            arcpy.SelectLayerByLocation_management('mhIdd_lyr', 'INTERSECT', riskRadius, "", 'NEW_SELECTION')
            # Test if any features are selected
            matchCountMHIDD = int(arcpy.GetCount_management('mhIdd_lyr')[0])
            # If no features selected, add message indicating no features selected
            if matchCountMHIDD == 0:
                arcpy.AddMessage('No MHIDD Facilities located within within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            else:
                # If features selected, export selected features to Excel
                arcpy.TableToExcel_conversion('mhIdd_lyr', outputFolder + r'\MHIDD_PATTS_{0}_{1}_{2}_{3}.xls'.format(pattsID, buffDistReplace, buffUnits, fileCount))
                # Add status message to ArcGIS dialog box
                arcpy.AddMessage('Completed extracting to Excel the MHIDD Facilities within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            # Schools
            # Select Schools sites that intersect SARA risk radius
            arcpy.SelectLayerByLocation_management('schools_lyr', 'INTERSECT', riskRadius, "", 'NEW_SELECTION')
            # Test if any features are selected
            matchCountSchools = int(arcpy.GetCount_management('schools_lyr')[0])
            # If no features selected, add message indicating no features selected
            if matchCountSchools == 0:
                arcpy.AddMessage('No Schools located within within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
            else:
                # If features selected, export selected features to Excel
                arcpy.TableToExcel_conversion('schools_lyr', outputFolder + r'\Schools_PATTS_{0}_{1}_{2}_{3}.xls'.format(pattsID, buffDistReplace, buffUnits, fileCount))
                # Add status message to ArcGIS dialog box
                arcpy.AddMessage('Completed extracting to Excel the Schools within the {0}-{1} risk radius for SARA facility PATTS {2}'.format(buffDist, buffUnits, pattsID))
    # If an error occurs running geoprocessing tool(s) capture error and write message
    # handle error outside of Python system
    except EnvironmentError as e:
        arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
        # Store information about the error
        tbE = sys.exc_info()[2]
        # add the line number the error occured to the log message
        arcpy.AddError('\nTool failed at Line {} in {}'.format(tbE.tb_lineno, sys.argv[0]))
        # add the error message to the log message
        arcpy.AddError('\nError: {}'.format(str(e)))
    # handle exception error
    except Exception as e:
        arcpy.AddError('\nAn error occured running this tool. Please provide the GIS Department the following error messages:')
        # Store information about the error
        tbE = sys.exc_info()[2]
        # add the line number the error occured to the log message
        arcpy.AddError('Tool failed at Line {} in {}'.format(tbE.tb_lineno, sys.argv[0]))
        # add the error message to the log message
        arcpy.AddError('\nError: {}'.format(e.message))
    finally:
        try:
            if cursor:
                del cursor
        except:
            pass