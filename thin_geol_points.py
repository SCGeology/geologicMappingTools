arcpy.env.addOutputsToMap = 0

points = arcpy.GetParameterAsText(0)
fishnet = arcpy.GetParameterAsText(1)
strike_dip_count = arcpy.GetParameterAsText(2)

desc = arcpy.Describe(points)
path = desc.path

arcpy.env.workspace = path

arcpy.AddMessage("Creating Spatial Join with Points and Fishnet")
spatial_join = arcpy.SpatialJoin_analysis(points, fishnet,"points_display","JOIN_ONE_TO_MANY","KEEP_ALL","#","INTERSECT","#","#")

arcpy.AddMessage("Adding Show/Hide Field")
arcpy.AddField_management(spatial_join,"show_hide","SHORT")

def fishnet_points(sj,sdc):
    #get the list of join JOIN FIDS from spatial join for create update cursors
    arcpy.AddMessage("Creating List of Join IDs")
    with arcpy.da.SearchCursor(sj,["JOIN_FID"]) as cursor:
        list = []
        for row in cursor:
            list.append(row[0])
        #make them unique list (set)
        jids = set(list)
        
    #iterate the JOIN IDs from the spatial join, creating update cursors for each subset 
    arcpy.AddMessage("Iterating each Join ID and select one point from each fishnet box, prioritizing points with more measurements.")
    for jid in jids:
        #this counter used for loop that prioritizes points with greater number of measurements
        startvalue = 0                   
        with arcpy.da.UpdateCursor(sj,["JOIN_FID",sdc,"show_hide"],"JOIN_FID ="+str(jid)) as cursor:
            for row in cursor:
                #will give show_hide a value of 1 for points with more measurements by comparing to startvalue.
                if row[1] > startvalue:
                    row[2] = 1
                    #increase start value
                    startvalue = row[1]
                else:
                    row[2] = 0
                cursor.updateRow(row)
        #iterate list another time to filter out points with smaller number of measurements, leaving only 1 per box in fishnet        
        with arcpy.da.UpdateCursor(sj,["JOIN_FID",sdc,"show_hide"],"JOIN_FID ="+str(jid)) as cursor:
            for row in cursor:
                if row[2] == 1 and row[1] == startvalue:
                    row[2] = 1
                else:
                    row[2] = 0
                cursor.updateRow(row)
                           
fishnet_points(spatial_join, strike_dip_count)