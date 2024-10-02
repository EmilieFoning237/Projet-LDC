from typing import Literal
from fpdf import FPDF
import json


class TiragePDF(FPDF):
    def __init__(
        self,
        orientation: Literal["P", "L"] = "L",
    ) -> None:
        super().__init__(orientation)
        self.logos = self.get_logos()

    def get_logos(self):
        with open("logos.json", "r") as file:
            return json.load(file)

    def add_background(self):
        pdf.image("medias/background.png", x=0, y=0, w=self.w, h=self.h)

    def title_page(self):
        pdf.set_xy(30, 15)
        self.set_font("Arial", "B", 28)
        self.set_text_color(255, 255, 255)
        pdf.cell(text="Tirage au sort de la ligue des champions", border=True)

    def center_element(self, axis: Literal["y", "x"], width: int):
        if axis == "x":
            return self.w / 2 - width / 2
        elif axis == "y":
            return self.h / 2 - width / 2
        else:
            raise Exception("La valeur saisie pour axis est incorrecte")

    def add_draw_team(self):
        w = 100
        y = self.center_element("y", w)
        pdf.image(f"logos/bayern_munich.png", x=30, y=y, w=w)

    def add_away(self):
        pdf.image("medias/plane.png", x=240, y=50, w=10)

    def add_home(self):
        pdf.image("medias/home.png", x=190, y=50, w=10)

    def add_opponents(self):
        y = 70
        for opponent in [
            "FC Barcelone",
            "Benfica Lisbonne",
            "Étoile Rouge de Belgrade",
            "Stade Brestois",
        ]:
            pdf.image(f"logos/{self.logos[opponent]}", x=180, y=y, h=20)
            y = y + 30
        y = 70
        for opponent in [
            "PSG",
            "Shakhtar Donetsk",
            "Feyenoord Rotterdam",
            "Bologne",
        ]:
            pdf.image(f"logos/{self.logos[opponent]}", x=240, y=y, h=20)
            y = y + 30

    def make_pdf(self):
        self.add_page()
        self.add_background()
        self.add_draw_team()
        self.title_page()
        self.add_home()
        self.add_away()
        self.add_opponents()
        self.output("tirage.pdf")


pdf = TiragePDF()
pdf.make_pdf()
