# Ce module contient la classe de tirage au sort.


class Draw:
    def __init__(self, teams: list[dict]) -> None:
        # Définissez les attributs dont vous aurez besoin
        self.teams = teams

    # Définissez les méthodes dont vous aurez besoin

    def make_draw(self):
        # Cette méthode sera celle appelée pour effectuer votre tirage au sort.
        print("Tirage au sort effectué")
