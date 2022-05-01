import os
import arcpy
from arcpy.sa import *
from feature import Feature


class City:
    def __init__(self, name):
        self.name = str(name)
        self.fcs = []
        self.spatial_reference = None
        self.final_raster = ""

        path = os.path.join(os.getcwd(), 'src', 'workspace')
        arcpy.env.workspace = path


    def set_spatial_reference(self, coord_system):
        try:
            sr = arcpy.SpatialReference(coord_system)
        except RuntimeError:
            print("Invalid spatial reference")
            return False
        self.spatial_reference = sr
        return True

    def add_feature_class(self, name):
        fc = Feature(name)
        # TODO fix preprocessing from breaking PolygontoRaster()
        #fc.preprocess(self.spatial_reference)
        fc.get_distances()
        fc.get_scores()
        fc.create_concentric_buffers()
        fc.buffers_to_raster()
        self.fcs.append(fc.add_rasters())

    def combine_feature_classes(self):
        file_out = self.name + '.tif'
        arcpy.CheckOutExtension("spatial")
        output = CellStatistics(self.fcs, 'SUM', 'DATA')
        output.save(file_out)
        arcpy.CheckInExtension("spatial")
        self.final_raster = file_out
        return file_out

    def save(self):
        path = os.path.join(os.getcwd(), 'src', 'cities', self.name)
        os.mkdir(path)
        arcpy.Copy_management(self.final_raster, os.path.join(path, 'score.tif'))
        for fc in self.fcs:
            arcpy.Copy_management(fc, os.path.join(path, fc))
        # TODO clean /workspace
