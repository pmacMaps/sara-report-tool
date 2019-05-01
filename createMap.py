#-------------------------------------------------------------------------------
# Name:        Lesson 29 - Building a Custom Geoprocessing Tool, Geospatial Programming
#
# Author:      Patrick McKinney, Harrisburg Area Community College
#
# Created:     4/25/19
#
#
# Updated:     5/1/19
# Description: sample script for getting a list of printer names and
#              printing a map document (.mxd).  Code sample was used
#              in the Python window of an open map document
#
# Copyright:   Harrisburg Area Community College, 2017#
#-------------------------------------------------------------------------------

# Import modules
import arcpy, os, errorLogger, datetime

def createSaraMap(sara_name,sara_address,patts,sara_site,risk_radii,output_dir):
    try:
        # create temporary layer file (.lyr) so the SARA Site can be added to the project map
        # you could delete this layer file at the end of the script if you wanted
        # make feature layer for SARA Site (created from input latitude/longitude)
        arcpy.MakeFeatureLayer_management(sara_site,'SARA_Site')
        # create a layer (.lyr) file
        # directory and name of layer file
        out_layer_file = r'{}\{} Site.lyr'.format(output_dir,sara_name)
        # save as a layer file
        arcpy.SaveToLayerFile_management('SARA_Site',out_layer_file,"RELATIVE")

        # create map document object for template map
        # make sure to del this variable to release the lock
        # update to r'C:\GIS\Scripts\SARA\Templates\SARA Radius Map Template.mxd'
        mxd_template = arcpy.mapping.MapDocument(r'F:\Scripts\ArcGIS Geoprocessing\SARA Tool\Templates\SARA Radius Map Template.mxd')
        # create a copy of the template map document
        project_mxd_file = os.path.join(output_dir, 'SARA_Project_Map.mxd')
        # save a copy of template map
        mxd_template.saveACopy(project_mxd_file)
        # add message
        arcpy.AddMessage('\nCreated a project map document')
        # create a map document object for county copy map
        # make sure to del this variable to release the lock
        project_mxd = arcpy.mapping.MapDocument(project_mxd_file)
        # create data frame object (so you can add a layer to a map)
        data_frame = arcpy.mapping.ListDataFrames(project_mxd)[0]

        # add exported streams layer to project map document
        # make sure to del this variable to release the lock
        # streams layer - this represents a layer file, not the layer as it is added to the map document
        sara_temp = arcpy.mapping.Layer(out_layer_file)
        # add streams to map document
        arcpy.mapping.AddLayer(data_frame,sara_temp,'TOP')
        # create object reference streams layer within map document
        sara_of_interest = arcpy.mapping.ListLayers(project_mxd,'*SARA*',data_frame)[0]
        # add layer to update symbology for streams layer on
        # make sure to del this variable to release the lock
        # update to r'C:\GIS\Scripts\SARA\Templates\SARA of Interest.lyr'
        sara_layer_file = arcpy.mapping.Layer(r'F:\Scripts\ArcGIS Geoprocessing\SARA Tool\Templates\SARA of Interest.lyr')
        # update symbology
        arcpy.mapping.UpdateLayer(data_frame,sara_of_interest,sara_layer_file,True)
        # select all records from county streams layer and zoom map to selected records and then unselect records

        # update map extent
        # applies to risk radius layer

        # make feature layer
        arcpy.MakeFeatureLayer_management(streams,'selectedStreams')
        # select records
        arcpy.SelectLayerByAttribute_management('selectedStreams','NEW_SELECTION',"OBJECTID > 0")
        # set map extent to all records in streams layer
        data_frame.extent = streams.getSelectedExtent()
        # unselect records so they don't appear as selected in map document or export to pdf
        arcpy.SelectLayerByAttribute_management('selectedStreams','CLEAR_SELECTION')
        # add message
        arcpy.AddMessage('\nAdded non-attaining streams for {} County to the map document and updated map extent\n'.format(county))
        # print 'Added non-attaining streams for {} County to the map document and updated map extent\n'.format(county)

        # update SARA Name for map
        sara_name_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Title_Text')[0]
        sara_name_text.text = str(sara_name)
        # update SARA Address for map
        sara_address_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Address_Text')[0]
        sara_address_text.text = str(sara_address)
        # update SARA PATTS for map
        sara_patts_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_PATTS_Text')[0]
        sara_patts_text.text = str(patts)
        # update date text element with current date
        # get current date
        date_today = datetime.date.today()
        # reformat date
        date_formatted = date_today.strftime("%m-%d-%Y")
        # create object reference to date text element
        date_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','Date_Text')[0]
        # update text
        date_text.text = str(date_today)

        # set column count for legend to 2
        #legend = arcpy.mapping.ListLayoutElements(countyMXD,'LEGEND_ELEMENT')[0]
        #legend.adjustColumnCount(2)

        # save map
        project_mxd.save()
        # add message
        arcpy.AddMessage('\nSaved the project map document')
        # print 'Saved map document {}\n'.format(mxdCopy)
        # export map to png using current date in file name
        # file name
        png_name = r'{} Risk Radius Map {}.png'.format(sara_name,date_today)
        # export map to pdf using default settings
        arcpy.mapping.ExportToPNG(project_mxd,os.path.join(output_dir,png_name),"PAGE_LAYOUT",resolution=300)
        # add message
        arcpy.AddMessage('\nExported project map to png format.  File is named {}'.format(png_name))
        # print 'Exported map to pdf at {}\n'.format(outputFolder)
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
            # delete variables to release locks on map documents (.mxd) and layer files (.lyr)
            del mxdTemplate,countyMXD,streamsTemp, symbologyStreams
            arcpy.AddMessage('\nReleased locks on map documents and layer files\n')
            # print 'Released locks on map documents and layer files'

            arcpy.AddMessage('\nCompleted running tool\n')
            # print 'Completed running tool'
        except:
            arcpy.AddWarning('\nLocks may still exist on map documents and layer files\n')
            # print 'Locks may still exist on map documents and layer files'

            arcpy.AddMessage('\nCompleted running tool\n')
            # print 'Completed running tool'