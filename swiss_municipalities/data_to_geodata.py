import geopandas
from geopandas import GeoDataFrame
from pandas import read_csv, DataFrame

from swiss_municipalities.typology_colormap import municipality_type_legend_handles
from swiss_municipalities.municipality_geodata import load_municipality_geodata
from swiss_municipalities.wgs84_to_lv03 import GPSConverter


def data_to_geodata(data: DataFrame) -> GeoDataFrame:
    """Converts dataframe with latitude and longitude columns to GeoDataFrame
    with points in the LV03 coordinate system"""
    converter = GPSConverter()

    if "latitude" not in data.columns or "longitude" not in data.columns:
        raise ValueError("Expected columns latitude and longitude in input DataFrame")

    x, y = list(zip(*data.apply(lambda row: converter.WGS84toLV03(row.latitude, row.longitude)[:2], axis=1)))
    geodata = geopandas.GeoDataFrame(
        data,
        geometry=geopandas.points_from_xy(
            x=x,
            y=y
        )
    )
    return geodata


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Load Municipality and City Data
    municipality_data = load_municipality_geodata()
    city_data = read_csv("./src/city_coordinates.csv")
    city_geodata = data_to_geodata(data=city_data)

    # Plot Municipalities
    ax = municipality_data.plot(
        color=municipality_data["COLOR"],
        edgecolor="#999999",
        linewidth=0.5,
        figsize=(15, 10)
    )

    ax.set_axis_off()
    plt.legend(handles=municipality_type_legend_handles)

    # Plot cities
    city_geodata.plot(ax=ax, color="black")

    for x_, y_, label in zip(city_geodata.geometry.x, city_geodata.geometry.y, city_geodata.city):
        ax.annotate(label, xy=(x_, y_), xytext=(5, 7), textcoords="offset points",
                    backgroundcolor=(1, 1, 1, 0.7))

    plt.show()
