import geopandas
from geopandas import GeoDataFrame
from pandas import read_csv

from swiss_municipalities.data_to_geodata import data_to_geodata
from swiss_municipalities.municipality_geodata import load_municipality_geodata
from swiss_municipalities.paths import abs_path


def add_municipality(geodata: GeoDataFrame) -> GeoDataFrame:
    municipality_data = load_municipality_geodata()
    geodata_with_municipalities = geopandas.sjoin(geodata, municipality_data, how="left", op="intersects")
    return geodata_with_municipalities


if __name__ == '__main__':
    city_data = read_csv(abs_path("src/city_coordinates.csv"))
    city_geodata = data_to_geodata(data=city_data)
    city_geodata_with_municipalities = add_municipality(city_geodata)
    print(city_geodata_with_municipalities[list(city_data.columns) + ["BFS_NUMMER", "TYPE"]])
