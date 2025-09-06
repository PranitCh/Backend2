import requests

pokemon_name = input("Enter Pokémon name: ").strip().lower()

poke_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
try:
    response = requests.get(poke_url, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Could not retrieve data for '{pokemon_name}':", e)
    exit(1)

poke_data = response.json()
types = [t['type']['name'] for t in poke_data['types']]
print(f"{pokemon_name.title()} Types: {', '.join(types)}")

local_server = "http://localhost:8000/"
multipliers_list = []

for ptype in types:
    url = f"{local_server}?attacker={ptype}"
    try:
        m_resp = requests.get(url, timeout=10)
        m_resp.raise_for_status()
    except Exception as e:
        print(f"Error contacting local server for type '{ptype}':", e)
        exit(1)
    multipliers_list.append(m_resp.json())

all_types = list(multipliers_list[0].keys())
combined_multipliers = {}

for defender in all_types:
    if len(multipliers_list) == 1:
        combined_multipliers[defender] = multipliers_list[0][defender]
    else:
        val = 1
        for m in multipliers_list:
            val *= m[defender]
        combined_multipliers[defender] = val

print("\nType effectiveness (combined):")
for t, v in combined_multipliers.items():
    print(f"{t.title():<10}: {v}x")
