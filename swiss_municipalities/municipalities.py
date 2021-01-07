# The id_to_type.json and id_to_name.json were scrapped from the official website of the Swiss "Bundesamf fur Statistik"
# https://www.atlas.bfs.admin.ch/maps/13/de/12360_12482_3191_227/20593.html
import json

with open("./src/id_to_type.json") as id_to_type_file:
    id_to_type_raw = json.load(id_to_type_file)

with open("./src/id_to_name.json") as id_to_name_file:
    id_to_name_raw = json.load(id_to_name_file)

id_to_type = {municipality_id.replace("|", ""): municipality_info["value"]
              for municipality_id, municipality_info in id_to_type_raw["values"].items()}

id_to_name = {municipality_id.replace("label_", ""): municipality_info["value"]
              for municipality_id, municipality_info in id_to_name_raw["943"]["111"].items()}
