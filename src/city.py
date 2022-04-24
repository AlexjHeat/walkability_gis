class City:
    def __init__(self, name):
        self.name = name
        self.fcs = []
        self.workspace = R"D:\Projects\PyCharmProjects\walkability_gis\src\workspace"
        # todo, create folder in /cities of city name, set workspace to it

    def add_feature_class(self):
        pass




#### Generating a raster from one feature class (shapefile) ####
# will create a ring of concentric buffers, with higher scores in the bands near the radius
# output will be a raster with varying scores based on proximity to feature class

#start, per feature class
    # clean files
        # remove all non-spatial fields
        # add field called 'SCORE', set to 1

    # create buffers
        # create a rings of n buffers around it, where n is the size of [distance1, distance2, distance3, ...]
        # dissolve buffers in parameters
        # return an array of the names of buffers

    # convert buffers to raster
        # base it on the field "SCORE"
        # each raster at this point should only have values of 0 or 1, and of the varying buffer sizes

    # add rasters
        # use raster math to combine rasters together
        # now we have 1 raster representing a heatmap of proximity to the original fc

# repeat for other feature class defined in criteria
# add rasters together, revealing a final raster showing the comprehensive score