import arcpy
import arcpy.management
from arcpy.sa import *


class Feature:
    def __init__(self, name):
        self.name = name
        self.fileName = name + ".shp"
        self.distances = ['0.25 mile', '0.5 mile', '1 mile', '2 mile']
        self.score = [1, 1, 1, 1]

    def get_distances(self):
        pass
        # TODO implement + validator

    def get_scores(self):
        pass
        # TODO implement + validator


    # Removes all non-spatial columns, adds a column called 'SCORE', initialized to 1
    # Handles any other necessary preprocessing
    # INPUT
    #   file_in: string - feature class to be cleaned & processed
    def preprocess(self):
        # Use self.rootFile
        pass
        # TODO make copy backup
        # TODO remove all fields
        # TODO any preprocessing, such as checking/changing projection


    # Creates multiple buffers, one for each entry in the input 'distances'
    # Dissolves all fields, then adds a field for SCORE, initiated to 1
    # INPUT
    #   file_in: string - feature class used to generate buffers
    #   distances: string[] - each element represents a distance used to create a buffer
    # OUTPUT
    #   buffer_list: string[] - A list of shapefile names for each buffer created
    def create_concentric_buffers(self):
        buffer_list = []
        for i in range(len(self.distances)):
            file_out = self.name + '_' + str(i) + '.shp'
            arcpy.Buffer_analysis(self.fileName, file_out, self.distances[i], dissolve_option='ALL')

            # Add 'SCORE' column
            arcpy.management.AddField(file_out, 'SCORE', 'SHORT')
            cursor = arcpy.UpdateCursor(file_out)
            for row in cursor:
                row.setValue('SCORE', 1)
                cursor.updateRow(row)
            del row
            del cursor

            buffer_list.append(file_out)
            # TODO initiate all rows of 'SCORE' to be based on score input array
        return buffer_list


    # Turns a buffer into a raster, based on a 'SCORE' field
    # INPUT
    #   file_in: string - feature class to be turned into a raster
    # OUTPUT
    #   file_out: string - Name of raster
    def buffer_to_raster(self, file_in, file_out):
        # TODO change parameters to generate file_out based on file_in
        # TODO Account for cell size
        arcpy.PolygonToRaster_conversion(file_in, 'SCORE', file_out)
        return file_out

    # Performs raster addition on all rasters available
    # INPUT
    #   files_in: string[] - rasters to be combined
    #   file_out: string - file name of output, combined raster
    # OUTPUT
    #   file_out: string - Name of raster
    def add_rasters(self, files_in, file_out):
        # TODO check if files_in[] is empty
        # TODO if array size is 1, return
        # TODO change parameters to generate file_out based on city object's name
        arcpy.CheckOutExtension("spatial")
        # output = arcpy.Raster(files_in[0])
        output = CellStatistics(files_in, 'SUM', 'DATA')
        # for raster in files_in[1:]:
        # output = output & arcpy.Raster(raster)
        output.save(file_out)
        arcpy.CheckInExtension("spatial")
        return file_out
