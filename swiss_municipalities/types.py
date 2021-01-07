import json

with open("./src/id_to_type.json") as id_to_type_file:
    id_to_type_raw = json.load(id_to_type_file)

id_to_type = {municipality_id.replace("|", ""): municipality_info["value"]
              for municipality_id, municipality_info in id_to_type_raw["values"].items()}
