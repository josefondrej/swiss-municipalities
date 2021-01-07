import geopandas as gpd
from geopandas import GeoDataFrame

from swiss_municipalities.colormap import type_to_color, municipality_type_legend_handles
from swiss_municipalities.names import id_to_name
from swiss_municipalities.types import id_to_type

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

    name_to_id = {value: key for key, value in id_to_name.items()}

    # The data sources do not match exactly with the municipalities
    # There were some mergers of municipalities into larger ones on 1st Jan 2020
    # Here we try to partially fix a few examples, but we were not able to fix all
    # https://en.wikipedia.org/wiki/Thurnen,_Bern
    # https://en.wikipedia.org/wiki/Villaz-Saint-Pierre
    # https://en.wikipedia.org/wiki/Villaz-Saint-Pierre
    # https://en.wikipedia.org/wiki/Prez-vers-Nor%C3%A9az
    name_to_id_fix = {
        "Verzasca": 5095,
        "Bergün Filisur": 3522,
        "La Punt Chamues-ch": 3785,
        "Stammheim": 36,
        "Prez": 2221,
        "Villaz": 2111,
        "Büsingen am Hochrhein": 7101,
        "Thurnen": 873,
        "Comunanza Cadenazzo/Monteceneri": 5391,
        "Campione d'Italia": 7301,
        "Comunanza Capriasca/Lugano": 5394
    }

    name_to_id.update(name_to_id_fix)

    data["ID"] = data["NAME"].apply(name_to_id.get)

    data["TYPE"] = data["ID"].apply(id_to_type.get)
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
