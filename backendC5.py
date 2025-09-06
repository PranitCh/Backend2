import requests

pokemon_name = input("Enter Pokémon name: ").strip().lower()
poke_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
response = requests.get(poke_url)
if response.status_code != 200:
    print(f"Pokémon '{pokemon_name}' not found.")
    exit(1)

poke_data = response.json()
types = [t['type']['name'] for t in poke_data['types']]

local_server_url = "http://localhost:8000"

if len(types) == 1:
    # Single-type Pokémon
    print(f"{pokemon_name.title()} Type: {types[0].title()}")
    multipliers = requests.get(f"{local_server_url}?defender={types[0]}").json()

    weak_2x = [t for t, v in multipliers.items() if v == 2]
    immunities = [t for t, v in multipliers.items() if v == 0]

    print("\n2× Weaknesses:" if weak_2x else "\n2× Weaknesses: None")
    if weak_2x:
        print(", ".join(sorted(weak_2x)))

    print("Immunities:" if immunities else "Immunities: None")
    if immunities:
        print(", ".join(sorted(immunities)))

elif len(types) == 2:
    # Dual-type Pokémon
    print(f"{pokemon_name.title()} Types: {types[0].title()}, {types[1].title()}")
    m1 = requests.get(f"{local_server_url}?defender={types[0]}").json()
    m2 = requests.get(f"{local_server_url}?defender={types[1]}").json()

    combined = {}
    for attack_type in m1.keys():
        combined[attack_type] = m1[attack_type] * m2.get(attack_type, 1)

    weak_4x = [t for t, v in combined.items() if v == 4]
    weak_2x = [t for t, v in combined.items() if v == 2]
    immunities = [t for t, v in combined.items() if v == 0]

    print("\n4× Weaknesses:" if weak_4x else "\n4× Weaknesses: None")
    if weak_4x:
        print(", ".join(sorted(weak_4x)))

    print("2× Weaknesses:" if weak_2x else "2× Weaknesses: None")
    if weak_2x:
        print(", ".join(sorted(weak_2x)))

    print("Immunities:" if immunities else "Immunities: None")
    if immunities:
        print(", ".join(sorted(immunities)))

else:
    print("Unexpected number of types found.")
