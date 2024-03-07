###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Gretchen Klock", "gklock"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):
    #Where workspace is the filepath for the geodatabase.
    try:
        import arcpy
            #this imports arcpy
        arcpy.env.workspace = workspace
            #this defines the workspace in arcpy as the inputted "workplace" file path
        fcList = arcpy.ListFeatureClasses()
            #this establishes the feature class list as the feature classes in the workspace
        for fc in fcList:
            desc= arcpy.Describe(fc)
                #this creates a Describe object
            if desc.shapeType=="Polygon":
                print(f"{desc.baseName} is a polygon feature class.")
                #every feature class that has the shape type polygon is printed.
            elif desc.shapeType=="Polyline":
                print(f"{desc.baseName} is a polyline feature class.")
                #every feature class that has the shape type polyline is printed.
            elif desc.shapeType=="Point":
                print(f"{desc.baseName} is a point feature class.")
                #every feature class that has the shape type point is printed.
            else: 
                print(f"{desc.baseName} is neither a polygon, point nor polyline feature class.")
                #all other feature classes are printed.
    except arcpy.ExecuteError:
       print(arcpy.GetMessages(2))

#printFeatureClassNames("S:\\2024_Spring\\GEOG_3050\\STUDENT\\gklock\\a2\\a2_data\\hw2.gdb")

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    #where inputFc is the filepath for a feature class and workspace is the filepath for the geodatabase.
    try:
        import arcpy
            #this imports arcpy
        arcpy.env.workspace = workspace
            #this defines the workspace in arcpy as the inputted "workplace" file path
        desc=arcpy.Describe(inputFc)
            #this creates a Describe object which pulls the properties of the input feature class (inputFc)
        fields=desc.fields
            #this establishes the fields object as the description of all the fields in the inputFc
        for field in fields:
            if field.type in ["Integer", "Float","OID","Double"]:
                #these are all the numeric field types
                print(f"{field.name} has a type of {field.type}")
    except arcpy.ExecuteError:
       print(arcpy.GetMessages(2))
       
#printNumericalFieldNames("S:\\2024_Spring\\GEOG_3050\\STUDENT\\gklock\\a2\\a2_data\\hw2.gdb\\bike_routes", "S:\\2024_Spring\\GEOG_3050\\STUDENT\\gklock\\a2\\a2_data\\hw2.gdb")

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    #Where input_geodatabase is the workspace, shapeType is "Point" "Polyline" or "Polygon" and output_geodatabase is the filepath for the database to be created. 
    try:
        import arcpy
            #this imports arcpy
        import os
            #this imports os (operating system) module
        arcpy.env.workspace = input_geodatabase
            #this defines the workspace in arcpy as the inputted "workplace" file path
        new_gdb = arcpy.CreateFileGDB_management(output_geodatabase, f"{shapeType}")
            #this creates a new geodatabase in the location of the output_geodatabase input with the name of the shape type input.
        fc_list = arcpy.ListFeatureClasses()
            #this establishes the feature class list as the feature classes in the workspace
        for shapefile in fc_list:
            desc= arcpy.Describe(shapefile)
                #this creates a Describe object
            if desc.shapeType==shapeType:
                #for feature classes where the shape type matches the input shape type
                out_featureclass = os.path.join(f"{new_gdb}", os.path.splitext(shapefile)[0])
                arcpy.management.CopyFeatures(shapefile, out_featureclass)
                    #this copies the feature class to the new geodatabase.
    except arcpy.ExecuteError:
       print(arcpy.GetMessages(2))
       
#exportFeatureClassesByShapeType('S:\\2024_Spring\\GEOG_3050\\STUDENT\\gklock\\a2\\a2_data\\hw2.gdb', "Point" ,'S:\\2024_Spring\\GEOG_3050\\STUDENT\\gklock\\a2\\a2_data')

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):
    #where inputFc is the filepath for a feature class, idFieldInputFc is the join key for the feature class, 
    #input table is the table to be joined, idFieldTable is the join key for the table and workspace is the filepath for the geodatabase.
    try:
        import arcpy
            #this imports arcpy
        arcpy.env.workspace = workspace
            #this defines the workspace in arcpy as the inputted "workplace" file path
        desc= arcpy.Describe(inputFc)
            #this creates a Describe object
        new_fc = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
            #this joins the input feature class and input table as a new feature class
        arcpy.conversion.ExportFeatures(new_fc, f"{desc.name}_joined")
            #this exports and saves the new feature class with the name of the input feature class plus _joined
        arcpy.management.ValidateJoin(inputFc, idFieldInputFc, inputTable, idFieldTable)
            #this validates the join
        print(arcpy.GetMessages())
            #this prints the join messages including the number of matches and total rows. 
        
    except arcpy.ExecuteError:
       print(arcpy.GetMessages(2))

#exportAttributeJoin('S:/2024_Spring/GEOG_3050/STUDENT/gklock/a2/a2_data/hw2.gdb/parks', 'PARK_ID', 'S:/2024_Spring/GEOG_3050/STUDENT/gklock/a2/a2_data/hw2.gdb/test_table.csv', 'PARK_ID', 'S:/2024_Spring/GEOG_3050/STUDENT/gklock/a2/a2_data/hw2.gdb')
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
