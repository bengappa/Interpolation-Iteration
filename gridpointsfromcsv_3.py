#
#       Grid Points from CSV 3
#       ---------------------------
#       Function reads a CSV of Grid Data and Turns it into a Point Shapefile
#       Handles Grid CSVs as they come from the Admin Site: Record, Longitude, Latitude, DepthInFeet
#
#
#       Benjamin Gappa
#       2/1/18
#
#
import arcpy

def csvToPoint(output_folder, output_name, csv_path_set, sr_set):
    """ Outer Function that runs the whole tool """
    import arcpy
    import csv
    from arcpy import env

    ## Functions
    def setEnv(out_folder):
        """ Sets basic environment variables """
        arcpy.env.workspace = out_folder
        arcpy.env.overwriteOutput = True # I've only ever wanted this to be true

    def shpPoint(out_folder, out_name, sr, **fields):
        """ Creates an empty Point Shapefile with option to add Fields """

        out_fc = out_fc = out_folder + "\\" + out_name + ".shp"
        arcpy.CreateFeatureclass_management(out_folder, out_name, "POINT", "", "", "", sr)

        for field in fields:
            arcpy.AddField_management(out_fc, field, fields[field])

    def shpInsert(out_fc, sr, csv_path):
        """ Uses and InsertCursor to write CSV data to a Point Shapefile """
        cursor = arcpy.InsertCursor(out_fc, sr)

        with open(csv_path, 'rb') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                feature = cursor.newRow()

                vertex = arcpy.CreateObject("Point")
                vertex.X = row['Longitude']
                vertex.Y = row['Latitude']
                feature.shape = vertex

                feature.DepthFt = row['DepthInFeet']
                feature.Record = row['Record']

                cursor.insertRow(feature)
        del cursor

    ## Nested function variables
    csv_path = csv_path_set
    sr = sr_set
    out_folder = output_folder
    out_name = output_name

    out_fc = out_folder + "\\" + out_name + ".shp"

    ## Set up workspace
    setEnv(out_folder)

    ## Create empty point shapefile
    field_dict = {"DepthFt" : "DOUBLE", "Record" : "LONG"}
    shpPoint(out_folder, out_name, sr, **field_dict)

    ## Fill the Shapefile
    shpInsert(out_fc, sr, csv_path)

##
## Run the Outer Function
##

# Variables
output_folder = str(arcpy.GetParameterAsText(0))
output_name = str(arcpy.GetParameterAsText(1))
csv_path_set = str(arcpy.GetParameterAsText(2))
sr_set = arcpy.GetParameterAsText(3)

# Run
csvToPoint(output_folder, output_name, csv_path_set, sr_set)
