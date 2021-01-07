import matplotlib.patches as mpatches

# Municipality type to color
type_to_color = {
    "11": "#c14a66",
    "12": "#d57685",
    "13": "#ecaaa7",
    "21": "#585796",
    "22": "#7d88b8",
    "23": "#a5badc",
    "31": "#418f5a",
    "32": "#81b684",
    "33": "#cadbad",

    "lake": "#cbf0fe",
    None: "#ffff00",
}

municipality_type_legend_handles = [mpatches.Patch(color=color, label=type or "missing") for type, color in type_to_color.items()]
