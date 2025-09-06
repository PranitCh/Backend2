import sys
import json
import requests

if len(sys.argv) > 1:
    output_file = sys.argv[1]
else:
    output_file = "output.json"

with open("/Users/pranit/Documents/Code/pokemon.txt", "r") as f:
    pokemon_list = [line.strip() for line in f if line.strip()]

results = {}

for identifier in pokemon_list:
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{identifier.lower()}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{identifier.lower()}"
    try:
        poke_resp = requests.get(poke_url)
        poke_data = poke_resp.json()
        species_resp = requests.get(species_url)
        species_data = species_resp.json()
    except Exception as e:
        continue

    abilities = [a["ability"]["name"] for a in poke_data.get("abilities", [])]

    types = [t["type"]["name"] for t in poke_data.get("types", [])]

    is_legendary = species_data.get("is_legendary", False)
    is_mythical = species_data.get("is_mythical", False)

    results[identifier] = {
        "Abilities": abilities,
        "Types": types,
        "Is Legendary": is_legendary,
        "Is Mythical": is_mythical
    }

with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"Data written to {output_file}")
