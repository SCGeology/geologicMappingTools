#for adding map unit to Stations point data in NCGMP09

Stations = arcpy.GetParameterAsText(0)
MapUnits = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True

desc = arcpy.Describe(Stations)
path = desc.path

arcpy.env.workspace = path

arcpy.AddMessage("Adding MapUnits to Point Data")
sj = arcpy.SpatialJoin_analysis(Stations, MapUnits, "SpatialJoin", "JOIN_ONE_TO_ONE", "KEEP_ALL") 

target = {}

with arcpy.da.SearchCursor(sj,["TARGET_FID","MapUnit_1"]) as cursor:
    for row in cursor:
        target[row[0]] = row[1]
        
with arcpy.da.UpdateCursor(Stations,["OBJECTID","MapUnit"]) as cursor:
    for row in cursor:
        row[1] = target[row[0]]
        cursor.updateRow(row)
        
arcpy.Delete_management(sj)        