#---------------------------------------------------------------------------------------------------------------------------------------------------------#
# Name:        Estimate Census Population for Risk Radius
#
# Ecosystem:   Used in SARAReportTool.py
#
# Purpose:     Create resident population estimates for each risk radius of a SARA facility
#
# Summary:     For each record in the SARA risk radii layer, the 2010  U.S. Census block dataset is clipped to the risk radius.  A proportional
#              residential population is calculated based upon how much of the block is within the risk radius.  A table is generated that calculates
#              the total proportional population within the risk radius.
#
#              The SARA risk radii layer is created in the previous module wihtin SARAReportTool.py (riskRadius.py)
#
# Author:      Patrick McKinney
#
# Created:     03/16/2016
#
# Updated:     4/4/2019
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

# Import modules
import arcpy, os, errorLogger

def updateProportionalValues(field_name, field_type, layer, message, calc_field):
    """add fields and calculate values for those created fields"""
    arcpy.AddField_management(layer, field_name, field_type)
    arcpy.AddMessage('\nAdded field "{}" for {}'.format(field_name,message))
    field_expression = '!{}! * !AREARATIO!'.format(calc_field)
    arcpy.CalculateField_management(layer, field_name, field_expression, 'PYTHON_9.3')
    arcpy.AddMessage('\nCompleted field calculation for field "{}"'.format(calc_field))

def createSummaryTable(table_name, summary_field, layer, message):
    """Create a summary table for a provided layer and field"""
    out_table = os.path.join(output_gdb, '{}_{}'.format(output_layer_name, table_name))
    stats_fields = [[summary_field, 'SUM']]
    arcpy.Statistics_analysis(layer, out_table, stats_fields)
    arcpy.AddMessage('\nCreated summary table for field "{}" for {}'.format(summary_field, patts_id))
    return out_table

def estimateCensusPopulation(riskRadius, patts_id, output_dir, output_gdb, results_text_file):
    """Calculate estimated population within each risk radius"""
    try:
        # allow data to be overwritten
        arcpy.env.overwriteOutput = True
        # Regional U.S. Census Blocks - clipping feature
        census_blocks = r'C:\GIS\Geodata.gdb\Regional_Census2010_Blocks_SPS'
        # placeholder for contents of text file storing estimate population
        text_file_contents = ''

        # fields for risk radius layer
        riskRadiusFields = ['Shape', 'PATTS', 'BUFFDIST', 'UNITS']
        # Search cursor for SARA Facility Risk Radii
        with arcpy.da.SearchCursor(riskRadius, riskRadiusFields) as cursor:
            for row in cursor:
                # Replace . with _ in buffer distance
                buffer_distance_replace = str(row[2]).replace('.', '_')
                # Buffer units and distance
                buffer_append_units = '{}_{}'.format(buffer_distance_replace, row[3])
                # layer name for results of clip
                output_layer_name = 'Estimated_Census_Population_PATTS_{}_{}'.format(row[1], buffer_append_units)
                # Boiler place text for ArcPy message
                message_text = 'PATTS {} risk radius {}-{}'.format(row[1], row[2], row[3])
                # Clip US Census Blocks layer by SARA Facility record
                clip_output_layer = arcpy.Clip_analysis(census_blocks, riskRadius, os.path.join(output_gdb, output_layer_name))
                # Add message that Clip is completed
                arcpy.AddMessage('\nCensus Blocks clipped for {}'.format(message_text))
                # Add field to hold clip area to original area ratio
                area_ratio_field_name = 'AREARATIO'
                area_ratio_field_type = 'DOUBLE'
                # Execut Add Field tool
                arcpy.AddField_management(clip_output_layer, area_ratio_field_name, area_ratio_field_type)
                # Add message that Area Ratio Field has been added
                arcpy.AddMessage('\nArea Ratio field added for {}'.format(message_text))
                # Calculate the new area to old area ratio for each Census Block
                area_ratio_field_expression = '!Shape_Area! / !ORAREA!'
                arcpy.CalculateField_management(clip_output_layer, 'AREARATIO', area_ratio_field_expression, 'PYTHON_9.3')
                # Add message that Area Ratio has been calculated
                arcpy.AddMessage('\nNew area to original area ratio calculated for {}'.format(message_text))
                # Add field for Estimated Population and calculate value
                updateProportionalValues('ESTPOP', 'LONG', clip_output_layer, message_text, 'POP10')
                # Add field for Estimated Households and calculate value
                updateProportionalValues('ESTHOUSEHOLDS', 'LONG', clip_output_layer, message_text, 'HOUSING10')
                # create summary table for Estimated Population
                est_pop_table = createSummaryTable('Sum_Population', 'ESTPOP', clip_output_layer, message_text)
                # create summary table for Estimated Housholds
                est_households_table = createSummaryTable('Sum_Households', 'ESTHOUSEHOLDS' , clip_output_layer, message_text)

                # get values in tables and write to text file

            # end for
        # end cursor
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
        try:
            if cursor:
                del cursor
        except:
            pass