from feature import Feature

class City:
    def __init__(self, name):
        self.name = name
        self.fcs = []
        self.workspace = R"D:\Projects\PyCharmProjects\walkability_gis\src\workspace"
        # todo, create folder in /cities of city name, set workspace to it

    def add_feature_class(self, name):
        fc = Feature(name)

        # TODO decide whether to implement getting and validating the distance and score data here or as feautre_class member functions
        fc.preprocess()
        fc.get_distances()
        fc.get_scores()

        buffer_list = fc.create_concentric_buffers()
        raster_list = []
        for buff in buffer_list:
            ras = fc.buffer_to_raster(buff, buff[:-4] + '.tif')
            raster_list.append(ras)
        fc.add_rasters(raster_list, 'output.tif')
        # TODO need dynamic output name
