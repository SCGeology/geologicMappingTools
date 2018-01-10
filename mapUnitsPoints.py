#for adding map unit to Stations point data in NCGMP09

Stations = arcpy.GetParameterAsText(0)
MapUnits = arcpy.GetParameterAsText(1)
uniqueID = arcpy.GetParameterAsText(2)

arcpy.env.overwriteOutput = True

arcpy.AddMessage("Adding MapUnits to Stations")

arcpy.SpatialJoin_analysis(Stations, MapUnits, "SpatialJoin", "JOIN_ONE_TO_ONE", "KEEP_ALL") 
arcpy.AddJoin_management(Stations, uniqueID, "SpatialJoin", uniqueID, "KEEP_ALL")
arcpy.CalculateField_management(Stations, Stations+".MapUnit", "!spatialJoin.MapUnit_1!", "PYTHON_9.3")
arcpy.RemoveJoin_management(Stations, "SpatialJoin")
arcpy.Delete_management("SpatialJoin","FeatureClass")
