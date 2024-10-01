import random
import json


class Draw:
    def __init__(self, data) -> None:
        self.teams: dict = data
        self.draw: dict = self.get_draw_format()
        self.pots: dict[str:list] = self.get_pot_lists()

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

    def is_in_pot(self, team: dict, pot: list):
        return team in pot

    def remove_team_in_same_league(self, team: dict, team_to_draw: list):
        new_team_to_draw = team_to_draw.copy()
        for t in team_to_draw:
            if t["pays"] == team["pays"]:
                new_team_to_draw.remove(t)
        return new_team_to_draw

    def remove_team_already_drawn(self, pot: str, kind: str, team_to_draw: list):
        new_team_to_draw = team_to_draw.copy()
        for team in team_to_draw:
            if self.draw[team["nom"]][pot][kind] != "":
                new_team_to_draw.remove(team)

        return new_team_to_draw

    def update_drawn_team_draw(
        self, draw_team: dict, drawn_team: dict, pot: str, kind: str
    ):
        pot = f"pot_{pot}"
        self.draw[drawn_team["nom"]][pot][kind] = draw_team

    def get_teams_to_draw(self, team: dict, pot_teams: list):
        # Récupération des équipe tirables.
        team_to_draw = pot_teams.copy()
        # On supprime l'équipe courante si elle est dans le pot qu'on tire
        if self.is_in_pot(team, pot_teams):
            team_to_draw.remove(team)
        # On supprime les équipes de la même ligue
        team_to_draw = self.remove_team_in_same_league(team, team_to_draw)
        return team_to_draw

    def make_draw(
        self, teams_to_draw: list, team_name: str, pot: str, kind: str, team: dict
    ):
        # Tirage
        drawn_team = random.choice(teams_to_draw)
        # Mise à jour du tirage
        self.draw[team_name][pot][kind] = drawn_team
        inverse = {"away": "home", "home": "away"}
        self.update_drawn_team_draw(team, drawn_team, team["chapeau"], inverse[kind])
        return drawn_team

    def get_draw(self) -> None:
        # tirage pour chaque équipe
        for team in self.teams:
            # Tirage de 2 équipe par pot
            for pot, pot_teams in self.pots.items():
                team_name = team["nom"]
                # On vérifie si le tirage est necessaire, c'est à dire que l'équipe a une string vide dans son tirage pour ce chapeau
                if (
                    self.draw[team_name][pot]["home"] != ""
                    and self.draw[team_name][pot]["away"] != ""
                ):
                    continue
                # Sinon on récupère les équipes tirables.
                else:
                    team_to_draw = self.get_teams_to_draw(team, pot_teams)

                # Si pas de tirage à domicile
                if self.draw[team_name][pot]["home"] == "":
                    # On récupère les équipes pouvant être tirées
                    team_to_draw_home = self.remove_team_already_drawn(
                        pot, "away", team_to_draw
                    )
                    # Tirage
                    drawn_team = self.make_draw(
                        team_to_draw_home, team_name, pot, "home", team
                    )
                    # Si pas non plus de tirage à l'exterieur, je retire l'équipe qui vient d'être tirée.
                    if self.draw[team_name][pot]["away"] == "":
                        team_to_draw.remove(drawn_team)

                # Si pas de tirage à l'exterieur
                if self.draw[team_name][pot]["away"] == "":
                    team_to_draw_away = self.remove_team_already_drawn(
                        pot, "home", team_to_draw
                    )
                    self.make_draw(team_to_draw_away, team_name, pot, "away", team)

                # Exportation dans un fichier json.
                with open("tirage.json", "w") as file:
                    json.dump(self.draw, file, ensure_ascii=False, indent=4)
