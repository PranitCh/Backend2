import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

resp = requests.get("https://pokeapi.co/api/v2/type/")
data = resp.json()
type_list = []
for t in data["results"]:
    type_list.append(t["name"])

matrix = {}
for defender in type_list:
    matrix[defender] = {}
    for attacker in type_list:
        matrix[defender][attacker] = 1

for defender in type_list:
    url = "https://pokeapi.co/api/v2/type/" + defender + "/"
    info = requests.get(url).json()
    for t in info["damage_relations"]["double_damage_from"]:
        matrix[defender][t["name"]] = 2
    for t in info["damage_relations"]["half_damage_from"]:
        matrix[defender][t["name"]] = 0.5
    for t in info["damage_relations"]["no_damage_from"]:
        matrix[defender][t["name"]] = 0

print(json.dumps(matrix, indent=2))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "attacker" in query and "defender" in query:
            attacker = query["attacker"][0].lower()
            defender = query["defender"][0].lower()
            if defender in matrix and attacker in matrix[defender]:
                out = {"attacker": attacker, "defender": defender, "multiplier": matrix[defender][attacker]}
            else:
                out = {"error": "Invalid type"}
        elif "defender" in query:
            defender = query["defender"][0].lower()
            if defender in matrix:
                out = {attacker: matrix[defender][attacker] for attacker in matrix[defender]}
            else:
                out = {"error": "Invalid type"}
        elif "attacker" in query:
            attacker = query["attacker"][0].lower()
            result = {}
            for defender in matrix:
                if attacker in matrix[defender]:
                    result[defender] = matrix[defender][attacker]
            out = result
        else:
            out = {"error": "Missing attacker or defender parameter"}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(out).encode())

pok_quer = input("Attacker/Defender: ")
pok_type = input("Enter the type of pokemon: ")

print("Building effectiveness matrix...")
print(f"Serving on http://localhost:8000/?{pok_quer.lower()}={pok_type.lower()}")
server = HTTPServer(('localhost', 8000), Handler)
server.serve_forever()

