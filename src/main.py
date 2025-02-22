import flet as ft
from othello import othello as oth

grille = ft.Column()
coup_joue = ()
joueur = 2
g = oth.creer_grille()

def main(page: ft.Page):
    page.title = "Othello"
    page.window_width = 400
    page.window_height = 400
    page.padding = 0
    page.spacing = 0

    def generate_grille(joueur: int, g: oth.grille) -> ft.Column:
        table = ft.Column(width=450, height=450, expand=True)

        for x in range(8):
            ligne = ft.Row()
            for y in range(8):
                if g[x][y] == 1:
                    ligne.controls.append(ft.Container(
                        content=ft.Column(controls=[ft.Text("⚪", size=20)], expand=True),
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN_300,
                        width=50,
                        height=50,
                    ))
                elif g[x][y] == 2:
                    ligne.controls.append(ft.Container(
                        content=ft.Column(controls=[ft.Text("⚫", size=20)], expand=True),
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN_300,
                        width=50,
                        height=50,
                    ))
                elif oth.peut_jouer((x, y), joueur, g):
                    ligne.controls.append(ft.Container(
                        content=ft.Column(controls=[ft.Text("🔹", size=20)], expand=True),
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN_300,
                        width=50,
                        height=50,
                        ink=True,
                        on_click=lambda e ,x=x ,y=y : jeu_onclick(e,x,y),
                    ))
                else:
                    ligne.controls.append(ft.Container(
                        width=50, height=50,
                        bgcolor=ft.colors.GREEN_300,
                    ))
            table.controls.append(ligne)

        return table

    def jeu_onclick(e, x : int, y: int):
        global coup_joue
        coup_joue = (x, y)
        jouer_coup()

    def jouer_coup():
        global grille, coup_joue, joueur, g
        if coup_joue in oth.coups_possibles(joueur, g):
            g = oth.jouer_coup(coup_joue, joueur, g)
            joueur = oth.autre(joueur)
            grille = generate_grille(joueur, g)
            page.controls[0] = grille
            page.update()

    grille = generate_grille(joueur, g)
    page.add(grille)
    page.update()

ft.app(main)
