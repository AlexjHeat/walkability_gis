import arcpy
import arcpy.management
from arcpy.sa import *
from .config import units, cell_size


class Feature:
    def __init__(self, name):
        self.name = name
        self.fileName = name + ".shp"
        self.distances = []
        self.score = []
        self.buffer_list = []
        self.raster_list = []


    def get_distances(self):
        while True:
            unit = raw_input('Please enter a unit: ')
            if unit in units:
                break
            print unit, 'is not a valid unit'

        values = raw_input("Please enter the distances in the form '0.25, 0.5, 1, 2': ").split(',')
        for i in range(len(values)):
            values[i] = values[i].strip()
            # TODO verify they're all numbers
            values[i] = values[i] + ' ' + unit
            self.distances.append(values[i])


    def get_scores(self):
        values = raw_input("Please enter the scores in the form '1, 1, 1, 1': ").split(',')
        for i in range(len(values)):
            values[i] = values[i].strip()
            self.score.append(int(values[i]))
            # TODO verify they're all numbers


    # Removes all non-spatial columns, adds a column called 'SCORE', initialized to 1
    # Handles any other necessary preprocessing
    # INPUT
    #   file_in: string - feature class to be cleaned & processed
    def preprocess(self, sa):
        arcpy.env.overwriteOutput = True
        arcpy.management.Project(self.fileName, "proj_" + self.fileName, sa)
        self.name = "proj_" + self.name
        self.fileName = "proj_" + self.fileName
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
                row.setValue('SCORE', self.score[i])
                cursor.updateRow(row)
            del row
            del cursor
            self.buffer_list.append(buf_out)
        return True


    # Turns a buffer into a raster, based on a 'SCORE' field
    # INPUT
    #   file_in: string - feature class to be turned into a raster
    # OUTPUT
    #   file_out: string - Name of raster
    def buffers_to_raster(self):
        for buff in self.buffer_list:
            ras_out = buff[:-4] + '.tif'
            arcpy.PolygonToRaster_conversion(buff, 'SCORE', ras_out,
                                             cell_assignment='MAXIMUM_COMBINED_AREA',
                                             cellsize=cell_size)
            self.raster_list.append(ras_out)
        return True

    # Performs raster addition on all rasters available
    # INPUT
    #   files_in: string[] - rasters to be combined
    #   file_out: string - file name of output, combined raster
    # OUTPUT
    #   file_out: string - Name of raster
    def add_rasters(self):
        file_out = self.name + '.tif'
        arcpy.CheckOutExtension("spatial")
        output = CellStatistics(self.raster_list, 'SUM', 'DATA')
        output.save(file_out)
        arcpy.CheckInExtension("spatial")
        return file_out
