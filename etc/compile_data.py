"""Run this if there is new data released, such as additional pokemon or moves."""
import requests


def compile_data():
    pokemon = {}
    base_stats, types, charged_moves, fast_moves = ([] for i in range(4))
    data_source = "https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-json-pokedex/master/output/pokemon.json"
    poke_data = requests.get(data_source).json()
    for mon in poke_data:
        for stat in mon["stats"].values():
            base_stats.append(stat)
        for poke_type in mon["types"]:
            types.append(poke_type["name"])
        for charged_move in mon["cinematicMoves"]:
            charged_moves.append(charged_move["name"])
        for fast_move in mon["quickMoves"]:
            fast_moves.append(fast_move["name"])
        pokemon[mon["name"]] = {"id_no": str(mon["dex"]), "maxCP": mon["maxCP"], "base_stats": base_stats,
                                "types": types, "charged_moves": charged_moves, "fast_moves": fast_moves}
        base_stats, types, charged_moves, fast_moves = ([] for i in range(4))
    return pokemon


with open("poke_dict.py", "w") as f:
    f.write("poke_dict = {\n")
    for key, values in compile_data().items():
        f.write('\t"' + key + '"' + ": " + str(values) + ",\n")
    f.write("}")
