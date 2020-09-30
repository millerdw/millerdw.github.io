from typing import Tuple
import geopandas as gpd
import glob
from os import path, getcwd


def merge_shapefiles(output_filepath,input_filepaths,
                     xlim:Tuple[float]=None,
                     ylim:Tuple[float]=None):
    """Take shapefiles from a directory or search string and merges into a single shapefile, filtered by x, y"""
    concatenated = gpd.GeoDataFrame(pd.concat((gpd.read_file(f) for f in glob.glob(input_filepaths)), 
                                              ignore_index=True))
    if (xlim is not None) and (ylim is not None):
        concatenated=concatenated.cx[xlim[0]:xlim[1],ylim[0]:ylim[1]]
    concatenated.to_file(output_filepath)



def main():
    merge_shapefiles(path.join(directory,'os_roads_local.shp'),
                 path.join(directory,'oproad_essh_gb/data/*_RoadLink.shp'),
                 (520000,575000),
                 (235000,280000))

    merge_shapefiles(path.join(directory,'os_greenspaces_local.shp'),
                     path.join(directory,'opgrsp_essh_tl/OS Open Greenspace (ESRI Shape File) TL/data/TL_GreenspaceSite.shp'),
                     (520000,575000),
                     (235000,280000))

    merge_shapefiles(path.join(directory,'os_rivers_local.shp'),
                     path.join(directory,'oprvrs_essh_gb/data/WatercourseLink.shp'),
                     (520000,575000),
                     (235000,280000))

    merge_shapefiles(path.join(directory,'airports.shp'),
                     path.join(directory,'DS_10283_2563/WorldAirports/export_airports.shp'),
                     (520000,575000),
                     (235000,280000))

    merge_shapefiles(path.join(directory,'railway_noise.shp'),
                 path.join(directory,'DEFRA_RailNoiseLAeq16hRound3_SHP_Full/data/Rail_Noise_LAeq16h_England_Round_3.shp'),
                 (520000,575000),
                 (235000,280000))

    merge_shapefiles(path.join(directory,'road_noise.shp'),
                     path.join(directory,'DEFRA_RoadNoiseLAeq16hRound3_SHP_Full/data/Road_Noise_LAeq16h_England_Round_3.shp'),
                     (520000,575000),
                     (235000,280000))


    merge_shapefiles(path.join(directory,'end_noise.shp'),
                     path.join(directory,'DEFRA_ENDNoiseMappingRound3_SHP_Full/data/Environmental_Noise_Directive_END_Noise_Mapping_Agglomerations_England_Round_3.shp'),
                     (520000,575000),
                     (235000,280000))