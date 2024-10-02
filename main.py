import json

from tirage import Draw

# Ouvrir et lire le fichier JSON
with open("teams.json", "r") as file:
    teams = json.load(file)

draw = Draw(teams)

draw.run()
