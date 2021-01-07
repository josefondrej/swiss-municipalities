# Swiss Municipalities

Small utility that can determine in
which [municipality](https://en.wikipedia.org/wiki/List_of_municipalities_of_Switzerland)
lie given coordinates in Switzerland and can also determine it's typology (e.g. agglomeration / rural area) and some
additional attributes. The underlying data was obtained from the websites of:

- [Bundesamt für Landestopografie](https://shop.swisstopo.admin.ch/de/products/landscape/boundaries3D)
- [Bundesamt für Statistik](https://www.atlas.bfs.admin.ch/maps/13/de/12360_12482_3191_227/20593.html)

## Requirements

Developed with `python = 3.8`, to install the required libraries run

```
python -m pip install -r requirements.txt
```

## Examples

### Municipality GeoData

The script `load_municipality_geodata.py` loads geographical data about Swiss municipalities as a geopandas
GeoDataFrame. This data contains some metadata about each municipality and then Polygon which gives boundaries of the
municipality in the Swiss LV03 system.

For basic example how to use this data try

```python
import matplotlib.pyplot as plt
from swiss_municipalities.municipality_geodata import load_municipality_geodata

geodata = load_municipality_geodata()
geodata.plot()
plt.show()
```

### WGS84 to LV03 Conversion

Often we don't get data in the LV03 system but rather in latitude and longitude. For this use the
script `data_to_geodata.py`
which expects dataframe with `latitude` and `longitude` columns -- e.g.

| city | latitude | longitude |
|------| ---------|-----------|
|Luzern|47.0541706|8.3047831|
|Ebikon|47.0849792|8.3461533|
|Stans|46.9602325|8.3684694|

and returns geopandas.GeoDataFrame with `geometry` column in the LV03 coordinates. For example:

```python
from pandas import read_csv
from swiss_municipalities.data_to_geodata import data_to_geodata

city_data = read_csv("./src/city_coordinates.csv")
city_geodata = data_to_geodata(data=city_data)
```

To convert WGS84 to LV03 we use the [converter by Harald von Waldow](https://github.com/hvwaldow/SwissGrid).

## Missing Data

For some municipalities we have missing data about the typology, you can check the state of the missing values on the
map below, which can be produced by going in the folder `swiss-municipalities` and running

```
python ./swiss_municipalities/load_data.py
```

![](src/map.png)
