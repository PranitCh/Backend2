import requests

pokemon_name = input("Enter Pokémon name: ").strip().lower()
poke_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
response = requests.get(poke_url)
poke_data = response.json()
types = [t['type']['name'] for t in poke_data['types']]

if len(types) != 2:
    print(f"{pokemon_name.title()} is not a dual-type Pokémon.")
    exit(0)

print(f"{pokemon_name.title()} Types: {types[0].title()}, {types[1].title()}")

local_server_url = "http://localhost:8000"

# Fetch multipliers for each type as defender
mult1 = requests.get(f"{local_server_url}?defender={types[0]}").json()
mult2 = requests.get(f"{local_server_url}?defender={types[1]}").json()

# Combine multipliers by multiplying
combined = {}
for attack_type in mult1.keys():
    combined[attack_type] = mult1[attack_type] * mult2.get(attack_type, 1)

# Categorize combined multipliers
weak_4x = [t for t, v in combined.items() if v == 4]
weak_2x = [t for t, v in combined.items() if v == 2]
immune_0x = [t for t, v in combined.items() if v == 0]

print("\n4× Weaknesses:", ", ".join(weak_4x) if weak_4x else "None")
print("2× Weaknesses:", ", ".join(weak_2x) if weak_2x else "None")
print("Immunities:", ", ".join(immune_0x) if immune_0x else "None")
