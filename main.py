# Ce module contient les instances de vos classes back et front end.
from draw import Draw
import json

with open("data/teams.json", "r") as file:
    teams = json.load(file)
# Création de votre instance de classe Draw
draw = Draw(teams)
draw.make_draw()
