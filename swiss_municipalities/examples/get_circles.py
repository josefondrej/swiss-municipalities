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


def expand_point_to_weighted_circle(center: Point, radius: float = 15000, point_density: int = 10,
                                    sigma: float = 0.5) \
        -> List[Tuple[Point, float]]:
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
    distances_from_center = [np.sqrt(((x - center_x) ** 2 + (y - center_y) ** 2))
                             for x, y in points_in_square]

    points_in_circle_with_dists = [
        ((x, y), r) for (x, y), r in zip(points_in_square, distances_from_center)
        if r <= radius]

    points_in_circle_with_weights = [
        ((x, y), 1 / np.sqrt(2 * np.pi) * np.exp(-r ** 2 / (2 * (sigma * radius) ** 2)))
        for ((x, y), r) in points_in_circle_with_dists
    ]

    total_weight = sum([w for ((x, y), w) in points_in_circle_with_weights])

    points_in_circle_with_weights = [(Point(x, y), w / total_weight) for ((x, y), w) in points_in_circle_with_weights]
    return points_in_circle_with_weights


def expand_point_to_circle(center: Point, radius: float = 15000, point_density: int = 10) \
        -> List[Point]:
    point_weights = expand_point_to_weighted_circle(center=center, radius=radius, point_density=point_density)
    points = [point for point, weight in point_weights]
    return points


def expand_points_to_circles(geodata: GeoDataFrame, radius: float = 10000, point_density: int = 10, sigma: float = 0.5,
                             add_weights: bool = False) -> GeoDataFrame:
    """Returns exploded dataframe where each row corresponds to some point in circle defined by center points
    in original dataframe and the radius a point density arguments"""
    geodata["circle"] = geodata["geometry"].apply(lambda point: expand_point_to_weighted_circle(
        center=point,
        radius=radius,
        point_density=point_density,
        sigma=sigma
    ))

    expanded_geodata = pd.DataFrame.explode(geodata, "circle")
    if add_weights:
        expanded_geodata["weight"] = expanded_geodata["circle"].apply(lambda x: x[1])
    expanded_geodata["circle"] = expanded_geodata["circle"].apply(lambda x: x[0])
    expanded_geodata = expanded_geodata.set_geometry("circle")
    expanded_geodata.drop(columns="geometry", inplace=True)
    expanded_geodata.rename(columns={"circle": "geometry"}, inplace=True)
    return expanded_geodata


if __name__ == '__main__':
    df = read_csv(abs_path("src/city_coordinates.csv"))
    geo_df = data_to_geodata(data=df)

    expanded_geo_df = expand_points_to_circles(geo_df, 15000, 8, add_weights=True)

    municipality_data = load_municipality_geodata()

    ax = municipality_data.plot(color="silver")
    ax.set_axis_off()
    expanded_geo_df.plot(ax=ax,
                         color=[(0, 191 / 255, 255 / 255, w * 50) for w in expanded_geo_df["weight"]],
                         markersize=1,
                         marker=".")
    plt.show()
