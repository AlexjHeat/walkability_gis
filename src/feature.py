import arcpy
import arcpy.management
from arcpy.sa import *


class Feature:
    def __init__(self, name):
        self.name = name
        self.fileName = name + ".shp"
        self.distances = ['0.25 mile', '0.5 mile', '1 mile', '2 mile']
        self.score = [1, 1, 1, 1]
        self.buffer_list = []
        self.raster_list = []


    def get_distances(self):
        # TODO move units to config
        units = ['mile', 'kilometer', 'feet', 'meter']
        while True:
            unit = raw_input('Please enter a unit: ')
            if unit in units:
                break
            print unit, 'is not a valid unit'

        while True:
            distances = raw_input("Please enter the distances in the form '0.25, 0.5, 1, 20'")
            # TODO split, trim, check they're all numbers


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
        # TODO any preprocessing, such as checking/changing projection


    # Creates multiple buffers, one for each entry in the input 'distances'
    # Dissolves all fields, then adds a field for SCORE, initiated to 1
    # INPUT
    #   file_in: string - feature class used to generate buffers
    #   distances: string[] - each element represents a distance used to create a buffer
    # OUTPUT
    #   buffer_list: string[] - A list of shapefile names for each buffer created
    def create_concentric_buffers(self):
        for i in range(len(self.distances)):
            buf_out = self.name + '_' + str(i) + '.shp'
            arcpy.Buffer_analysis(self.fileName, buf_out, self.distances[i], dissolve_option='ALL')

            # Add 'SCORE' column
            arcpy.management.AddField(buf_out, 'SCORE', 'SHORT')
            cursor = arcpy.UpdateCursor(buf_out)
            for row in cursor:
                row.setValue('SCORE', 1)
                cursor.updateRow(row)
            del row
            del cursor

            self.buffer_list.append(buf_out)
            # TODO initiate all rows of 'SCORE' to be based on score input array
        return True


    # Turns a buffer into a raster, based on a 'SCORE' field
    # INPUT
    #   file_in: string - feature class to be turned into a raster
    # OUTPUT
    #   file_out: string - Name of raster
    def buffers_to_raster(self):
        # TODO change parameters to generate file_out based on file_in
        # TODO Account for cell size
        for buff in self.buffer_list:
            ras_out = buff[:-4] + '.tif'
            arcpy.PolygonToRaster_conversion(buff, 'SCORE', ras_out,
                                             cell_assignment='MAXIMUM_COMBINED_AREA',
                                             cellsize=0.001)
            # TODO make sure cell size is fine, put it in config
            self.raster_list.append(ras_out)
        return True

    # Performs raster addition on all rasters available
    # INPUT
    #   files_in: string[] - rasters to be combined
    #   file_out: string - file name of output, combined raster
    # OUTPUT
    #   file_out: string - Name of raster
    def add_rasters(self, file_out):
        # TODO check if files_in[] is empty
        # TODO if array size is 1, return
        # TODO change parameters to generate file_out based on city object's name
        arcpy.CheckOutExtension("spatial")
        # output = arcpy.Raster(files_in[0])
        output = CellStatistics(self.raster_list, 'SUM', 'DATA')
        # for raster in files_in[1:]:
        # output = output & arcpy.Raster(raster)
        output.save(file_out)
        arcpy.CheckInExtension("spatial")
        return file_out
