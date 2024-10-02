# Ce module contient la classe de tirage au sort.


class Draw:
    def __init__(self, teams: list[dict]) -> None:
        # Définissez les attributs dont vous aurez besoin
        self.teams = teams
        self.pots = self.get_pot_lists()
        self.draw = self.get_draw_format()
        pass

    def get_draw_format(self) -> list:
        draw = {}
        for team in self.teams:
            name_team = team["nom"]
            draw[name_team] = {
                "pot_1": {"home": "", "away": ""},
                "pot_2": {"home": "", "away": ""},
                "pot_3": {"home": "", "away": ""},
                "pot_4": {"home": "", "away": ""},
            }

        return draw

    def get_pot_lists(self) -> dict[str:list, str:list, str:list, str:list]:
        pot1, pot2, pot3, pot4 = [], [], [], []

        for team in self.teams:
            if team["chapeau"] == 1:
                pot1.append(team)
            elif team["chapeau"] == 2:
                pot2.append(team)
            elif team["chapeau"] == 3:
                pot3.append(team)
            elif team["chapeau"] == 4:
                pot4.append(team)
        return {"pot_1": pot1, "pot_2": pot2, "pot_3": pot3, "pot_4": pot4}

    # Définissez les méthodes dont vous aurez besoin

    def make_draw(self):
        # Cette méthode sera celle appelée pour effectuer votre tirage au sort.
        print("Tirage au sort effectué")
