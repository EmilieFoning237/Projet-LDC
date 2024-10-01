import json
import random

from tirage import Draw

# Ouvrir et lire le fichier JSON
with open("teams.json", "r") as file:
    teams = json.load(file)

draw = Draw(teams)

draw.get_draw()
