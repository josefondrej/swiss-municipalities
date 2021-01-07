import json
from statistics import mode

with open("./src/id_to_type.json") as id_to_type_file:
    id_to_type_raw = json.load(id_to_type_file)

id_to_typology = {int(municipality_id.replace("|", "")): municipality_info["value"]
                  for municipality_id, municipality_info in id_to_type_raw["values"].items()}

# Manually rewrote from wikipedia, e.g.
# https://en.wikipedia.org/wiki/Villaz,_Switzerland -- copy the SFOS number of the municipalities that resulted in the
# merged one
_merged_municipalities = {
    5399: [5135, 5129, 5102, 5095, 5105],  # Verzasca
    3544: [3521, 3522],  # Bergün Filisur
    3714: [3691, 3693, 3694],  # Rheinwald
    5287: [5286, 5285, 5284, 5283],  # Riviera
    6417: [6402, 6409, 6410, 6411, 6414, 6415],  # La Grande-Béroche
    293: [134, 140],  # Wädenswil
    295: [132],  # Horgen
    294: [222],  # Elgg
    292: [44, 36, 42],  # Stammheim
    2237: [2185, 2213, 2221],  # Prez
    2117: [2111, 2116],  # Villaz
    889: [873, 874, 876],  # Thurnen

    # For the following there is just no typology to be found anywhere
    5391: None,  # Comunanza Cadenazzo/Monteceneri
    5394: None,  # Comunanza Capriasca/Lugano
    2391: None,  # Staatswald Galm -- does not belong to any municipality
}

_merged_id_to_typology = {munic_id: mode(list(map(id_to_typology.get, former_ids))) if former_ids is not None else None
                          for munic_id, former_ids in _merged_municipalities.items()}

id_to_typology.update(_merged_id_to_typology)
