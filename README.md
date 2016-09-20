# Introduction

This repository contains the set of Python scripts that were developed to create a custom [ArcGIS geoprocessing tool](http://desktop.arcgis.com/en/arcmap/10.3/main/analyze/geoprocessing-tools.htm) to assit the Cumberland County, PA Department of Public Safety with their [SARA Tier II](https://www.epa.gov/epcra/state-tier-ii-reporting-requirements-and-procedures) reporting.

The goal of this repository to is to provide a starting point for similar analyses.  The dataset and geodatabase variables will need to be updated to the specifications of your project.  You will also need to create your own ArcGIS toolbox for your implementation of this tool.

While created for a specific purpose, the scripts can be refactored to perform a proximity analysis for a location that is defined by latitude/longitude.  It can estimate the popluation within a certain distance of that facility (buffer), and select features from other layers that are within the buffer.


# Summary of Tool

This tool consists of four Python scripts.  `SARAReportTool.py` is the script that the custom tool is built from.  The other three scripts are modules which are imported into `SARAReportTool.py`.  I will provide a summary of what each script does.

Each module uses [try-except statements](http://pro.arcgis.com/en/pro-app/arcpy/get-started/error-handling-with-python.htm) and logs errors to the tool window.


### SARAReportTool.py

This tool collects parameters from the ArcGIS tool's form using the `arcpy.GetParameterAsText()` [method](http://pro.arcgis.com/en/pro-app/arcpy/functions/getparameterastext.htm).  All inputs are required.

1. Latitude (double format) - the latitude in decimal degrees of the SARA facility.
2. Longitude (double format) - the longitude in decimal degrees of the SARA facility.
3. PATTS ID (string format) - an unique identifier for each SARA facility
4. Distances for Risk Radius (double format, multiple values allowed) - the distance(s) for each risk radius buffer
5. Risk Radius Units (string format) - the units for the risk radius buffers
6. Folder location (folder format) - the folder location for the Microsoft Excel spreadsheets created that list the vulnerable facilities that intersect each risk radius.

These inputs are used in the three analyses.  The first analysis calculate a [multi-ring buffer](http://pro.arcgis.com/en/pro-app/tool-reference/analysis/multiple-ring-buffer.htm) around the SARA facility using the distances and units provided in the form.

The second analysis clips a Census geography (blocks) to each risk radius using a `Search Cursor` [(more  info)](http://pro.arcgis.com/en/pro-app/arcpy/functions/searchcursor.htm).  A proportional population value is calculated for each Census block, and the sum of the proportional population is added to a table.

The third analysis performs a [Select by Location](http://desktop.arcgis.com/en/arcmap/10.3/map/working-with-layers/using-select-by-location.htm) analysis on each vulnerable facility for each risk radius.  If any vulnerable facilities intersect the risk radius, those features are exported to a Microsoft Excel file.


### riskRadius.py

This tool creates the risk radii for the SARA facility using a function that is imported into `SARAReportTool.py`.  

The first step is to create a [Point](http://pro.arcgis.com/en/pro-app/arcpy/classes/point.htm) and then a [Geometry Point](http://pro.arcgis.com/en/pro-app/arcpy/classes/pointgeometry.htm) from the user entered latitude and longitude from the tool's form.

Next, the [Project](https://pro.arcgis.com/en/pro-app/tool-reference/data-management/project.htm) tool is run to convert the point from WGS 1984 to Pennsylvania State Plane South (ft).  You will need to update the script to use the coordinate system in your locale.  

Finally, the multi-ring buffer tool is run against the projected point using the distances and units provided in the form.  The output for this tool is defined in a geodatabase, and the naming convetion uses the unique PATTS ID in the naming convetion.

The output layer is also returned from the function, as the layer is used as an input for the other tools.


### populatioEstimate.py

This tool estimates the population located within each risk radius generated from `riskRadius.py`.  The tool is a function that is imported into `SARAReportTool.py`.  

You will need to update the variable that stores the Census geography used in your implementation of this tool.  You will also need to create a double field called *ORAREA* to store the original (pre-clippped) area of each census geography.

The tool uses a Search Cursor on the output layer from the multi-ring buffer tool.  For each record in this layer, the Census geography layer is [clipped](http://pro.arcgis.com/en/pro-app/tool-reference/analysis/clip.htm).

The ratio of original area to clipped area for each feature is calculated.  The population field for the Census geography is multiplied by the ratio value to create a proportional value.

That is, if 50% of the Census block is within the risk radius, then we will assume 50% of that block's population is within the risk radius.   This is a limitation of using aggregate data such as Census blocks.

Each output from the Clip operation is output into a geodatabase that you will need to update the variable for.  The name of the feature class is created using PATTS ID, buffer distance and units, and a count variable to help avoid duplicate names.

Lastly, a table for each output of the Clip operation is created that calculates the sum of the proportional popluation.  


### vulnerableFacilities.py

This tool identifies any vulnerable facilities that intersect each risk radius. The tool is a function that is imported into `SARAReportTool.py`.

The tool uses a Search Cursor on the output layer from the multi-ring buffer tool. You will need to update the variables for vulnerable facilities.

For any vulnerable facilities that are within the risk radius, the selected features are exported to a Microsoft Excel file using the [`arcpy.TableToExcel_conversion()` method](http://pro.arcgis.com/en/pro-app/tool-reference/conversion/table-to-excel.htm).  If no features are selected, a message is added to the ArcGIS tool window.