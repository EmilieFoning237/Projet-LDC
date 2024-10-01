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
        return {"pot1": pot1, "pot2": pot2, "pot3": pot3, "pot4": pot4}

    def is_in_pot(self, team: dict, pot: list):
        return team in pot

    def get_team_in_same_league(self, team, pot):
        same_league_teams = []
        for t in pot:
            if t["pays"] == team["pays"]:
                same_league_teams.append(t)

    def get_team_already_drawn(self, pot: str, kind: str):
        teams_already_drawn = []
        for team, _ in self.draw.items():

            if self.draw[team][pot][kind] != "":
                for t in self.teams:
                    if t["nom"] == team:
                        teams_already_drawn.append(t)
                    else:
                        continue

        return teams_already_drawn

    def update_drawn_team_draw(
        self, draw_team: dict, drawn_team: dict, pot: str, kind: str
    ):

        self.draw[drawn_team["nom"]][pot][kind] = draw_team

    def get_draw(self) -> None:
        for pot, pot_teams in self.pots.items():
            for team in self.teams:
                team_name = team["nom"]
                if self.is_in_pot(team, pot_teams):
                    team_to_draw = pot_teams.remove(team)
                else:
                    team_to_draw = pot_teams
                same_league_teams = self.get_team_in_same_league(team, pot_teams)
                team_to_draw = [
                    team for team in team_to_draw if team not in same_league_teams
                ]

                already_home_drawn_teams = self.get_team_already_drawn(pot, "home")
                already_away_drawn_teams = self.get_team_already_drawn(pot, "away")
                team_to_draw_home = [
                    team
                    for team in team_to_draw
                    if team not in already_home_drawn_teams
                ]

                team_to_draw_away = [
                    team
                    for team in team_to_draw
                    if team not in already_away_drawn_teams
                ]

                home_drawn_team = random.choice(team_to_draw_home)
                self.draw[team_name]["pot_1"]["home"] = home_drawn_team
                self.update_drawn_team_draw(team_name, home_drawn_team, pot, "away")

                away_drawn_team = random.choice(team_to_draw_away)
                self.draw[team_name]["pot_1"]["away"] = away_drawn_team
                self.update_drawn_team_draw(team_name, away_drawn_team, pot, "home")

        # Exportation dans un fichier json.
        with open("self.draw.json", "w") as file:
            json.dump(self.draw, file, ensure_ascii=False, indent=4)
