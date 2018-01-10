# This tool is developed for use with the GeMS data model toolbox.
# The tool searches feature classes and tables for fields whose terms are required to be defined in the Glossary table,
# and inserts the values from those fields in to the Glossary. 

import arcpy

#~~~~~
#get parameters from dialog box
gdb = arcpy.GetParameterAsText(0)
dataset1 = arcpy.GetParameterAsText(1)
dataset2 = arcpy.GetParameterAsText(2)
dataset3 = arcpy.GetParameterAsText(3)
#~~~~~

# global variables
arcpy.env.workspace = gdb
datasets = [dataset1, dataset2, dataset3]
# the list below are fields outlined in the NCGMP09 documentation whose terms must be defined in the glossary.
list = ["Type", "IdentityConfidence", "ExistenceConfidence", "LocationMethod", "ParagraphStyle", "PartType", "Property", "PropertyValue", "Qualifier", "Event", "TimeScale", "ProportionTerm", "AgeUnits","ScientificConfidence","AreaFillPatternDescription"]

glossary = gdb + "/Glossary"

# Adds a field in Glossary for showing the source field of the term, if it doesn't already exist.
# This is helpful to know when defining the terms.
# When the 'delete identical' tool is run at the end of the script, any two terms identical terms from different source fields will remain.
# However, all terms in glossary should be unique, so you can pinpoint and troubleshoot your error. 
fieldList = arcpy.ListFields(glossary, "TermSrcFld")
fieldCount = len(fieldList)
if (fieldCount == 0):
    arcpy.AddMessage("Adding TermSrcField to Glossary")
    arcpy.AddField_management(glossary, "TermSrcFld", "TEXT") 
else:
    arcpy.AddMessage("TermSrcFld field exists.")

# iterates through datasets (chosen by user in dialog box), then feature classes, then fields for unique values.
for dataset in datasets:
    if dataset != "none":
        arcpy.AddMessage("Searching Feature Classes in dataset: " + dataset)
        fcs1 = arcpy.ListFeatureClasses("*", "All", dataset)
        for fc in fcs1:
            # If the field names from 'list' exist in a dataset or table, the unique values are listed and written to the glossary table.
            fields = arcpy.ListFields(fc, "*", "All")
            for field in fields:
                if field.name in list:
                    fldName = field.name
                    fcName = fc
                    myValues = set([row.getValue(fldName) for row in arcpy.SearchCursor(fcName,fields=fldName)])
                    arcpy.AddMessage("***Writing " + str(len(myValues)) + " unique values in the " + str(field.name) + " field of feature class " + str(fc) + " to Glossary***")
                    cursor = arcpy.da.InsertCursor(glossary, ("Term", "TermSrcFld"))
                    for value in myValues:
                        cursor.insertRow([value,field.name])
                    del cursor

# Same process as above, but for all tables in the geodatabase.
# For basic GeMS databases, results will rreturn from AT LEAST the DescriptionOfMapUnits table.
arcpy.AddMessage("Searching Tables")
tables = arcpy.ListTables("*", "All")
for table in tables:
    fields = arcpy.ListFields(table, "*", "All")
    for field in fields:
        if field.name in list:
            fldName = field.name
            tableName = table
            myValues = set([row.getValue(fldName) for row in arcpy.SearchCursor(tableName,fields=fldName)])
            arcpy.AddMessage("***Writing " + str(len(myValues)) + " unique values in the " + str(field.name) + " field of table " + str(table) + " to Glossary***")
            cursor = arcpy.da.InsertCursor(glossary, ("Term", "TermSrcFld"))
            for value in myValues:
                if value != None:
                    cursor.insertRow([value,field.name])
            del cursor
          
arcpy.AddMessage("Deleting identical values in the Glossary table")
arcpy.DeleteIdentical_management(glossary, ["Term", "TermSrcFld"])
