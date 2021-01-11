from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from pandas import read_csv
from shapely.geometry import Point

from swiss_municipalities.data_to_geodata import data_to_geodata
from swiss_municipalities.municipality_geodata import load_municipality_geodata
from swiss_municipalities.paths import abs_path


def expand_point_to_circle(center: Point, radius: float = 15000, point_density: int = 10) \
        -> List[Tuple[float, float]]:
    """
    Return point grid in circle(center, radius) with ~ points_on_radius lying on the circle's radius
    :param center: center of circle, x, y
    :param radius: circle radius, if the coordinate system is LV03 this corresponds approximately to meters
    :param point_density: how many points lie approximately on the radius

    Example
    This is how such a circle could look like
          + + + +
        + + + + + +
        + + + + + +
        + + + + + +
          + + + +
    """
    center_x, center_y = center.x, center.y
    delta = radius / point_density
    points_in_square = [(center_x + i * delta, center_y + j * delta)
                        for i in range(-point_density, point_density + 1)
                        for j in range(-point_density, point_density + 1)]
    points_in_circle = [(x, y) for x, y in points_in_square if
                        np.sqrt(((x - center_x) ** 2 + (y - center_y) ** 2)) <= radius]
    points_in_circle = [Point(x, y) for x, y in points_in_circle]
    return points_in_circle


def expand_points_to_circles(geodata: GeoDataFrame, radius: float = 10000, point_density: int = 10) -> GeoDataFrame:
    """Returns exploded dataframe where each row corresponds to some point in circle defined by center points
    in original dataframe and the radius a point density arguments"""
    geodata["circle"] = geodata["geometry"].apply(lambda point: expand_point_to_circle(
        center=point,
        radius=radius,
        point_density=point_density
    ))

    expanded_geodata = pd.DataFrame.explode(geodata, "circle")
    expanded_geodata = expanded_geodata.set_geometry("circle")
    expanded_geodata.drop(columns="geometry", inplace=True)
    expanded_geodata.rename(columns={"circle": "geometry"}, inplace=True)
    return expanded_geodata


if __name__ == '__main__':
    df = read_csv(abs_path("src/city_coordinates.csv"))
    geo_df = data_to_geodata(data=df)

    expanded_geo_df = expand_points_to_circles(geo_df, 15000, 8)

    municipality_data = load_municipality_geodata()

    ax = municipality_data.plot(color="gray")
    ax.set_axis_off()
    expanded_geo_df.plot(ax=ax, color="#20e9ff", markersize=1, marker=".", alpha=0.5)
    plt.show()
