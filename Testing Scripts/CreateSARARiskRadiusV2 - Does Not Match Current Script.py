#----------------------------------------------------------------------------------------------#
# Name:        Create SARA Risk Radii
#
# Purpose:     Create risk radii for a user selected SARA facility
#
# Summary:     User enters the PATTS ID for the facility, buffer distances, and buffer units.
#              The script checks to see if the input PATTS ID exists in the SARA layer.
#              If so, the script runs a multi-ring buffer within a try/except block.
#
# Author:      Patrick McKinney
# Created:     03/17/2016
# Copyright:   (c) Cumberland County GIS 2016
# Licence:     <your licence>
#----------------------------------------------------------------------------------------------#

# Import arcpy
import arcpy

# User entered variables from ArcGIS tool

# user entered latitude
# convert from text to float
lat = float(arcpy.GetParameterAsText(0))

# user entered longitude
# convert from text to float
lon = float(arcpy.GetParameterAsText(1))

# PATTS ID
pattsID = arcpy.GetParameterAsText(2)

# Buffer distances
mrbDistances = arcpy.GetParameterAsText(3)

# Buffer units - will typically be miles or feet
mrbUnits = arcpy.GetParameterAsText(4)


# Variables for Project tool

# Spatial References
# WGS 1984
srWGS84 = arcpy.SpatialReference(4326)

# NAD 1983
srNAD83 = arcpy.SpatialReference(2272)

# Output
# Create file GDB for these layers
outputNAD83 = r'\\CCPASR07\ncgs$\Scripts\ArcGIS Geoprocessing\SARA Tool\SARA_Tool_DEV.gdb\InputPoint_NAD83_{}'.format(pattsID)


try:
    # create point
    point = arcpy.Point(lon, lat)

    # create geometry point
    geometryPoint = arcpy.PointGeometry(point, srWGS84)

    # Convert WGS 1984 layer to a NAD 1983 layer
    arcpy.Project_management(geometryPoint, outputNAD83, srNAD83, "NAD_1983_To_WGS_1984_1", preserve_shape = "PRESERVE_SHAPE")

    # Multi-ring Buffer tool

    # Output layer
    mrbOutput = r'\\Ccpasr34\psep$\GIS\SARA\RiskRadii.gdb\RiskRadii_PATTS_{}'.format(pattsID)

    # Field name in output layer to store buffer distance
    mrbDistanceField = 'BUFFDIST'

    # Dissolve option
    mrbDissolveOption = 'NONE'

    # Run tool
    arcpy.MultipleRingBuffer_analysis(outputNAD83,mrbOutput,mrbDistances,mrbUnits,mrbDistanceField,mrbDissolveOption)

    # Add message that Multiple Ring Buffer tool complete
    arcpy.AddMessage('SARA Risk Radii created')

    # Add Field Managment Tool
    # Add field to output layer with buffer distance units
    fieldName = 'UNITS'
    fieldType = 'TEXT'
    fieldExpression = '"{0}"'.format(mrbUnits)

    # Execut Add Field Management tool
    arcpy.AddField_management(mrbOutput, fieldName,fieldType)

    # Add message that Units field added to layer
    arcpy.AddMessage('UNITS field added')

    # Calculate Field Managment Tool
    # Calculate buffer distance units
    arcpy.CalculateField_management(mrbOutput, fieldName, fieldExpression, 'PYTHON_9.3')

    # Add message that buffer distance units added to Units field
    arcpy.AddMessage('The units ' + mrbUnits + ' added to the UNITS field')

except Exception:
        e = sys.exc_info()[1]
        arcpy.AddError(e.args[0])