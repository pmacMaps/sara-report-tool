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
# Updated:     5/13/2019
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
    field_expression = '!{}! * !AREARATIO!'.format(calc_field)
    arcpy.CalculateField_management(layer, field_name, field_expression, 'PYTHON_9.3')

def createSummaryTable(gdb, base_layer, table_name, summary_field, layer, message):
    """Create a summary table for a provided layer and field"""
    out_table = os.path.join(gdb, '{}_{}'.format(base_layer, table_name))
    stats_fields = [[summary_field, 'SUM']]
    arcpy.Statistics_analysis(layer, out_table, stats_fields)
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

        # make feature layer for risk radii buffer to enable select by attribute
        arcpy.MakeFeatureLayer_management(riskRadius, 'Buffer Layer')
        # fields for risk radius layer
        riskRadiusFields = ['OBJECTID', 'PATTS', 'BUFFDIST', 'UNITS']
        # Search cursor for SARA Facility Risk Radii
        with arcpy.da.SearchCursor(riskRadius, riskRadiusFields) as cursor:
            for row in cursor:
                # where clause
                whereClause = "OBJECTID = {}".format(row[0])
                # select the current record from the buffer layer using OBJECTID
                # this will set each select by location to be run against the current feature in the buffer layer
                arcpy.SelectLayerByAttribute_management('Buffer Layer', 'NEW_SELECTION', whereClause)
                # Replace . with _ in buffer distance
                buffer_distance_replace = str(row[2]).replace('.', '_')
                # Buffer units and distance
                buffer_append_units = '{}_{}'.format(buffer_distance_replace, row[3])
                # layer name for results of clip
                output_layer_name = 'Estimated_Census_Data_PATTS_{}_{}'.format(row[1], buffer_append_units)
                # Boiler place text for ArcPy message
                message_text = 'PATTS {} risk radius {}-{}'.format(row[1], row[2], row[3])
                # Clip US Census Blocks layer by SARA Facility record
                clip_output_layer = arcpy.Clip_analysis(census_blocks, 'Buffer Layer', os.path.join(output_gdb, output_layer_name))
                # Add message that Clip is completed
                arcpy.AddMessage('\nCensus Blocks clipped for {}'.format(message_text))
                # Add field to hold clip area to original area ratio
                area_ratio_field_name = 'AREARATIO'
                area_ratio_field_type = 'DOUBLE'
                # Execut Add Field tool
                arcpy.AddField_management(clip_output_layer, area_ratio_field_name, area_ratio_field_type)
                # Calculate the new area to old area ratio for each Census Block
                area_ratio_field_expression = '!Shape_Area! / !ORAREA!'
                arcpy.CalculateField_management(clip_output_layer, 'AREARATIO', area_ratio_field_expression, 'PYTHON_9.3')
                # Add field for Estimated Population and calculate value
                updateProportionalValues('ESTPOP', 'LONG', clip_output_layer, message_text, 'POP10')
                # Add field for Estimated Households and calculate value
                updateProportionalValues('ESTHOUSEHOLDS', 'LONG', clip_output_layer, message_text, 'HOUSING10')
                # create summary table for Estimated Population
                est_pop_table = createSummaryTable(output_gdb, output_layer_name,'Sum_Population', 'ESTPOP', clip_output_layer, message_text)
                # create summary table for Estimated Housholds
                est_households_table = createSummaryTable(output_gdb, output_layer_name, 'Sum_Households', 'ESTHOUSEHOLDS' , clip_output_layer, message_text)
                # Add Message
                arcpy.AddMessage('\nCompleted calculating estimated 2010 U.S. Census Population and Households for {}'.format(message_text))
                # write estimated population to text file
                text_file_contents += '\nEstimated 2010 Census population within {}-{} risk radius is '.format(row[2],row[3])
                with arcpy.da.SearchCursor(est_pop_table, ['SUM_ESTPOP']) as pop_cursor:
                    for line in pop_cursor:
                        text_file_contents += '{}\n'.format(int(line[0]))
                # write estimated households to text file
                text_file_contents += '\nEstimated 2010 Census households within {}-{} risk radius is '.format(row[2],row[3])
                with arcpy.da.SearchCursor(est_households_table, ['SUM_ESTHOUSEHOLDS']) as households_cursor:
                    for line in households_cursor:
                        text_file_contents += '{}\n'.format(int(line[0]))
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
            with open(results_text_file, 'a') as f:
                f.write(str(text_file_contents))
            if cursor:
                del cursor
        except:
            arcpy.AddError('\nThere was an error writing the population and households results message to the project text file')