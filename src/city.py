import os
import arcpy
from feature import Feature

class City:
    def __init__(self, name):
        self.name = str(name)
        self.fcs = []
        self.spatial_reference = None

        path = os.path.join(os.getcwd(), 'src', 'cities', self.name)
        os.mkdir(path, 0o666)
        self.workspace = path
        arcpy.env.workspace = self.workspace

    def set_sr(self, sr):
        try:
            arcpy.SpatialReference(sr)
        except RuntimeError:
            print("Invalid spatial reference")
            return False
        self.spatial_reference = sr
        return True

    def add_feature_class(self, name):
        fc = Feature(name)

        # TODO decide whether to implement getting and validating the distance and score data here or as feautre_class member functions
        fc.preprocess()
        # fc.get_distances()
        # fc.get_scores()
        fc.create_concentric_buffers()
        fc.buffers_to_raster()
        fc.add_rasters('output.tif')
        # TODO need dynamic output name

