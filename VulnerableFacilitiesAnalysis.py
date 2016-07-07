#---------------------------------------------------------------------------------------------------------------------------------#
# Name:        Vulnerable Facilities Analysis for Risk Radius
#
# Purpose:     Create an excel spreadsheet of vulnerable facilities located within risk radii.
#              Vulnerable facilities include schools, daycares, medical facilities, assisted living centers, and MHIDD facilities
#
# Summary:     User selects a SARA risk radius layer.  For each record in that layer, a select by location analysis is run on each
#              vulnerable facility.  The selected features are exported to an excel spreadsheet at a located defined by the user.#

# Author:      Patrick McKinney
# Created:     04/28/2016
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#----------------------------------------------------------------------------------------------------------------------------------#

import arcpy

# User selects risk radii layer as input for analysis
sara = arcpy.GetParameterAsText(0)
# User selects output folder
outputFolder = arcpy.GetParameterAsText(1)

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

try:
    cursor = arcpy.SearchCursor(sara, fields="NAME; BUFFDIST; UNITS") # old cursor syntax
    fileCount = 0
    for row in cursor:
        fileCount += 1
        # Assisted Living
        # Select Assisted Living sites that intersect SARA risk radius
        arcpy.SelectLayerByLocation_management('assistedLiving_lyr', 'INTERSECT', sara, "", 'NEW_SELECTION')
        # Export selected features to Excel
        arcpy.TableToExcel_conversion('assistedLiving_lyr', outputFolder + r'\AssistedLiving_{0}_{1}_{2}_{3}.xls'.format(row.getValue('NAME'), row.getValue('BUFFDIST'), row.getValue('UNITS'), fileCount))
        # Add status message to ArcGIS dialog box
        arcpy.AddMessage('Completed extracting to Excel the Assisted Living Facilities within the {0}-{1} risk radius for {2} SARA facility'.format(row.getValue('BUFFDIST'), row.getValue('UNITS'),row.getValue('NAME')))
        # Daycares
        # Select Daycares sites that intersect SARA risk radius
        arcpy.SelectLayerByLocation_management('daycares_lyr', 'INTERSECT', sara, "", 'NEW_SELECTION')
        # Export selected features to Excel
        arcpy.TableToExcel_conversion('daycares_lyr', outputFolder + r'\Daycares_{0}_{1}_{2}_{3}.xls'.format(row.getValue('NAME'), row.getValue('BUFFDIST'), row.getValue('UNITS'), fileCount))
        # Add status message to ArcGIS dialog box
        arcpy.AddMessage('Completed extracting to Excel the Daycares within the {0}-{1} risk radius for {2} SARA facility'.format(row.getValue('BUFFDIST'), row.getValue('UNITS'),row.getValue('NAME')))
        # Health Medical
        # Select Health Medical sites that intersect SARA risk radius
        arcpy.SelectLayerByLocation_management('medical_lyr', 'INTERSECT', sara, "", 'NEW_SELECTION')
        # Export selected features to Excel
        arcpy.TableToExcel_conversion('medical_lyr', outputFolder + r'\MedicalSites_{0}_{1}_{2}_{3}.xls'.format(row.getValue('NAME'), row.getValue('BUFFDIST'), row.getValue('UNITS'), fileCount))
        # Add status message to ArcGIS dialog box
        arcpy.AddMessage('Completed extracting to Excel the Medical Facilities within the {0}-{1} risk radius for {2} SARA facility'.format(row.getValue('BUFFDIST'), row.getValue('UNITS'),row.getValue('NAME')))
        # MHIDD
        # Select MHIDD sites that intersect SARA risk radius
        arcpy.SelectLayerByLocation_management('mhIdd_lyr', 'INTERSECT', sara, "", 'NEW_SELECTION')
        # Export selected features to Excel
        arcpy.TableToExcel_conversion('mhIdd_lyr', outputFolder + r'\MHIDD_{0}_{1}_{2}_{3}.xls'.format(row.getValue('NAME'), row.getValue('BUFFDIST'), row.getValue('UNITS'), fileCount))
        # Add status message to ArcGIS dialog box
        arcpy.AddMessage('Completed extracting to Excel the MHIDD Facilities within the {0}-{1} risk radius for {2} SARA facility'.format(row.getValue('BUFFDIST'), row.getValue('UNITS'),row.getValue('NAME')))
        # Schools
        # Select Schools sites that intersect SARA risk radius
        arcpy.SelectLayerByLocation_management('schools_lyr', 'INTERSECT', sara, "", 'NEW_SELECTION')
        # Export selected features to Excel
        arcpy.TableToExcel_conversion('schools_lyr', outputFolder + r'\Schools_{0}_{1}_{2}_{3}.xls'.format(row.getValue('NAME'), row.getValue('BUFFDIST'), row.getValue('UNITS'), fileCount))
        # Add status message to ArcGIS dialog box
        arcpy.AddMessage('Completed extracting to Excel the Schools within the {0}-{1} risk radius for {2} SARA facility'.format(row.getValue('BUFFDIST'), row.getValue('UNITS'),row.getValue('NAME')))
    del cursor, row

except Exception:
    e = sys.exc_info()[1]
    arcpy.AddError(e.args[0])