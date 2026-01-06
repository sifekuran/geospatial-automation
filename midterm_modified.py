import arcpy

homepath = r"C:\Users\sifek\OneDrive - Northern Arizona University\GSP-535 Class\Ex02\midterm" # defines a home path
arcpy.env.workspace = homepath + "Oil_project.gdb"                                        # sets a workspace environment
arcpy.env.overwriteOutput = True                                                          # allows overwriting output

# create a parcel feature layer (a temporary in-memory object)
parcel_layer = arcpy.management.MakeFeatureLayer("Parcels", "Parcellyr")

# list the well path feature classes in the geodatabase
wellpathlist = arcpy.ListFeatureClasses(feature_type="Polyline", feature_dataset="Well Data")
for wellpath in wellpathlist:
    print("\nProcessing well path", wellpath + " ...")  # message when a well path is ready to process

    print("   Buffering the well path ...")
    wellbuf = "Buffers/" + wellpath + "_buffer"         # create an output buffer feature class name
    if arcpy.Exists(wellbuf):                           # checks existence of a well buffer if it exists
        arcpy.management.Delete(wellbuf)                # deletes the well buffer if it exists
    # call the Buffer tool to create a 200-foot buffer around the well path
    well_buffer = arcpy.analysis.Buffer(wellpath, wellbuf, "200 Feet")

    # call the SelectLayerByLocation tool to select parcels that intersect the well path buffer
    print("   Selecting parcels intersecting the well buffer ...")
    parcels_selected = arcpy.management.SelectLayerByLocation(parcel_layer, "INTERSECT", well_buffer)

    print("   Extracting mailing list...")
    mail_file = homepath + "mailing_list_" + wellpath + ".txt"

    with open(mail_file, "w") as fileout:
        with arcpy.da.SearchCursor(parcels_selected, ["Prop_add"]) as cursor:
            for row in cursor:
                if row[0]:
                    fileout.write(row[0] + "\n")


print("Mailing lists created successfully!")
print("Check them out in folder", homepath)
