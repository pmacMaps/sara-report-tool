#-------------------------------------------------------------------------------
# Name:        Create SARA Facility Map and PNG Export
#
# Author:      Patrick McKinney
#
# Created:     4/25/19
#
#
# Updated:     5/7/19
#-------------------------------------------------------------------------------

# Import modules
import arcpy, os, errorLogger, datetime

def saveLayerFile(layer,name,out_dir):
        # create a feature layer
        arcpy.MakeFeatureLayer_management(layer,name)
        # directory and name of layer file
        out_layer_file = r'{}\{}.lyr'.format(out_dir, name)
        # save as a layer file
        arcpy.SaveToLayerFile_management(name,out_layer_file,"RELATIVE")
        # get access to layer file
        return out_layer_file

def createSaraMap(sara_site, risk_radii, sara_name, sara_address, patts, output_dir):
    try:
        # create a layer file to disk for SARA Facility
        sara_lyr = saveLayerFile(sara_site,'SARA_Site',output_dir)
        # create a layer file to disk for Risk Radii
        risk_radii_lyr = saveLayerFile(risk_radii,'Risk_Radii',output_dir)

        # Delete this section after you validate function works

        # create temporary layer file (.lyr) so the SARA Site can be added to the project map
        # you could delete this layer file at the end of the script if you wanted
        # make feature layer for SARA Site (created from input latitude/longitude)
        #arcpy.MakeFeatureLayer_management(sara_site,'SARA_Site')
        # create a layer (.lyr) file
        # directory and name of layer file
        #out_layer_file_sara = r'{}\{} Site.lyr'.format(output_dir,sara_name)
        # save as a layer file
        #arcpy.SaveToLayerFile_management('SARA_Site',out_layer_file_sara,"RELATIVE")

        # create temporary layer file (.lyr) so the Risk Radii can be added to the project map
        # you could delete this layer file at the end of the script if you wanted
        # make feature layer for Risk Radii (created from input latitude/longitude)
        #arcpy.MakeFeatureLayer_management(risk_radii,'Risk_Radii')
        # create a layer (.lyr) file
        # directory and name of layer file
        #out_layer_file_radii = r'{}\Risk Radii.lyr'.format(output_dir)
        # save as a layer file
        #arcpy.SaveToLayerFile_management('Risk_Radii',out_layer_file_radii,"RELATIVE")

        # create map document object for template map
        # update to r'C:\GIS\Scripts\SARA\Templates\SARA Radius Map Template.mxd'
        mxd_template = arcpy.mapping.MapDocument(r'F:\Scripts\ArcGIS Geoprocessing\SARA Tool\Templates\SARA Radius Map Template.mxd')
        # create a copy of the template map document
        project_mxd_file = os.path.join(output_dir, 'SARA_Project_Map.mxd')
        # save a copy of template map
        mxd_template.saveACopy(project_mxd_file)
        # add message
        arcpy.AddMessage('\nCreated a project map document')
        # create a map document object for project map
        project_mxd = arcpy.mapping.MapDocument(project_mxd_file)
        # create data frame object (so you can add a layer to a map)
        data_frame = arcpy.mapping.ListDataFrames(project_mxd)[0]

        # add SARA Facility to map document
        # make sure to del this variable to release the lock
        # sara layer file on disk - this represents a layer file, not the layer as it is added to the map document
        sara_temp = arcpy.mapping.Layer(sara_lyr)
        # add layer to map document
        arcpy.mapping.AddLayer(data_frame,sara_temp,'TOP')
        # create object reference streams layer within map document
        sara_of_interest = arcpy.mapping.ListLayers(project_mxd,'*SARA*',data_frame)[0]
        # add symbology layer
        # update to r'C:\GIS\Scripts\SARA\Templates\SARA of Interest.lyr'
        sara_symbol_file = arcpy.mapping.Layer(r'F:\Scripts\ArcGIS Geoprocessing\SARA Tool\Templates\SARA of Interest.lyr')
        # update symbology
        arcpy.mapping.UpdateLayer(data_frame,sara_of_interest,sara_symbol_file,True)

        # add risk radii to map
        # make sure to del this variable to release the lock
        # risk radii layer file on disk - this represents a layer file, not the layer as it is added to the map document
        risk_radii_temp = arcpy.mapping.Layer(risk_radii_lyr)
        # add layer to map document
        arcpy.mapping.AddLayer(data_frame,risk_radii_temp,'TOP')
        # create object reference streams layer within map document
        risk_radii_of_interest = arcpy.mapping.ListLayers(project_mxd,'*Risk*',data_frame)[0]
        # add symbology layer
        # update to r'C:\GIS\Scripts\SARA\Templates\Risk Radii.lyr'
        risk_radii_symbol_file = arcpy.mapping.Layer(r'F:\Scripts\ArcGIS Geoprocessing\SARA Tool\Templates\Risk Radii.lyr')
        # update symbology
        arcpy.mapping.UpdateLayer(data_frame,risk_radii_of_interest,risk_radii_symbol_file,True)

        # update map extent
        arcpy.MakeFeatureLayer_management(risk_radii_of_interest, 'Risk_Radii_Map')
        # select records
        arcpy.SelectLayerByAttribute_management('Risk_Radii_Map','NEW_SELECTION',"OBJECTID > 0")
        # set map extent to all records in risk radii layer
        data_frame.extent = risk_radii_of_interest.getSelectedExtent()
        # unselect records so they don't appear as selected in map document or export to png
        arcpy.SelectLayerByAttribute_management('Risk_Radii_Map','CLEAR_SELECTION')

        # update SARA Name for map
        sara_name_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Title_Text')[0]
        sara_name_text.text = str(sara_name)
        # update SARA Address for map
        sara_address_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_Address_Text')[0]
        sara_address_text.text = str(sara_address)
        # update SARA PATTS for map
        sara_patts_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','SARA_PATTS_Text')[0]
        sara_patts_text.text = sara_patts_text.text.replace('x', str(patts))
        # update date text element with current date
        # get current date
        date_today = datetime.date.today()
        # reformat date
        date_formatted = date_today.strftime("%m-%d-%Y")
        # create object reference to date text element
        date_text = arcpy.mapping.ListLayoutElements(project_mxd,'TEXT_ELEMENT','Date_Text')[0]
        # update text
        date_text.text = str(date_formatted)

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
            del mxd_template, project_mxd, sara_lyr, sara_temp, sara_symbol_file, risk_radii_lyr, risk_radii_temp, risk_radii_symbol_file
            arcpy.AddMessage('\nReleased locks on map documents and layer files')
            arcpy.AddMessage('\nCompleted running tool')
        except:
            arcpy.AddWarning('\nLocks may still exist on map documents and layer files')
            arcpy.AddMessage('\nCompleted running tool')