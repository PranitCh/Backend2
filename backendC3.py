import requests

pokemon_name = input("Enter Pokémon name: ").strip().lower()
poke_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
response = requests.get(poke_url)
poke_data = response.json()
types = [t['type']['name'] for t in poke_data['types']]

if len(types) != 1:
    print(f"{pokemon_name.title()} is not a single-type Pokémon.")
    exit(0)

ptype = types[0]
print(f"{pokemon_name.title()} Type: {ptype.title()}")

local_server_url = "http://localhost:8000/"
url = f"{local_server_url}?defender={ptype}"
multipliers = requests.get(url).json()

weak_2x = [attacker for attacker, mult in multipliers.items() if mult == 2]
immune_0x = [attacker for attacker, mult in multipliers.items() if mult == 0]

print("\n2× Weaknesses:", ", ".join(weak_2x) if weak_2x else "None")
print("Immunities:", ", ".join(immune_0x) if immune_0x else "None")
