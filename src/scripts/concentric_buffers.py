import arcpy
import arcpy.management



arcpy.env.workspace = "C:\Users\Insano\Downloads"


def clean_fc(file_in):
    # TODO make copy backup
    # TODO remove all fields
    arcpy.management.AddField(file_in, 'SCORE', 'SHORT')
    # TODO initiate all rows to 1 for 'SCORE'


def create_concentric_buffers(file_in, distances):
    buffer_list = []
    for i in range(len(distances)):
        file_out = file_in[:-4] + '_' + str(i) + '.shp'
        arcpy.Buffer_analysis(file_in, file_out, distances[i], dissolve_option='ALL')
        buffer_list.append(file_out)
        arcpy.management.AddField(file_out, 'SCORE', 'SHORT')
    return buffer_list


def buffer_to_raster(shapefile_in, shapefile_out):
    arcpy.PolygonToRaster_conversion(shapefile_in, 'SCORE', shapefile_out)

# clean_fc('railroads.shp')
#create_concentric_buffers("railroads.shp", ['1 Mile'])
buffer_to_raster('railroads_0.shp', 'test.tif')
print("done")
