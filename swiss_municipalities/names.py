import json

with open("./src/id_to_name.json") as id_to_name_file:
    id_to_name_raw = json.load(id_to_name_file)

id_to_name = {municipality_id.replace("label_", ""): municipality_info["value"]
              for municipality_id, municipality_info in id_to_name_raw["943"]["111"].items()}
