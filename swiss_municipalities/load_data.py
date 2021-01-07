import geopandas as gpd
from geopandas import GeoDataFrame

from swiss_municipalities.colormap import type_to_color, municipality_type_legend_handles
from swiss_municipalities.typologies import id_to_typology

_lake_names = [
    "Lac Léman (VD)",
    "Bodensee (TG)",
    "Lac de Neuchâtel (NE)",
    "Zürichsee (ZH)",
    "Thunersee",
    "Bodensee (SG)",
    "Lac de Neuchâtel (VD)",
    "Bielersee (BE)",
    "Brienzersee",
    "Lac de Neuchâtel (VD)",
    "Bodensee (TG)",
    "Lac Léman (VD)",
    "Herzogenbuchsee",
    "Lac de Neuchâtel (VD)",
    "Münchenbuchsee",
    "Lac de Joux",
    "Greifensee",
    "Lac de Morat (VD)",
    "Gerzensee",
    "Mauensee",
    "Geuensee",
    "Sursee",
    "Ermensee",
    "Greifensee",
    "Lac de Neuchâtel (BE)",
    "Bodensee (TG)",
    "Bielersee (NE)"
]


def _is_lake(name: str) -> bool:
    is_lake = name in _lake_names
    return is_lake


def get_data() -> GeoDataFrame:
    data = gpd.read_file("./src/swissBOUNDARIES3D_1_3_TLM_HOHEITSGEBIET.shp")

    # We are only interested in Swiss Municipalities
    data = data[data["ICC"] == "CH"]

    data["TYPE"] = data["BFS_NUMMER"].apply(id_to_typology.get)
    data.loc[data["NAME"].apply(_is_lake), "TYPE"] = "lake"

    data["COLOR"] = data["TYPE"].apply(type_to_color.get)
    return data


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    test_data = get_data()

    base = test_data.plot(
        color=test_data["COLOR"],
        edgecolor="#999999",
        linewidth=0.5,
        figsize=(15, 10)
    )

    # plt.title("Municipalities of Switzerland", size=25)
    base.set_axis_off()
    plt.legend(handles=municipality_type_legend_handles)
    plt.tight_layout()
    plt.savefig("./src/map.png")
