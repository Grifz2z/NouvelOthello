import flet as ft
from othello import othello as oth
from othello import ia 
import time
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
                        bgcolor=ft.Colors.GREEN_300,
                        width=50,
                        height=50,
                    ))
                elif g[x][y] == 2:
                    ligne.controls.append(ft.Container(
                        content=ft.Column(controls=[ft.Text("⚫", size=20)], expand=True),
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.GREEN_300,
                        width=50,
                        height=50,
                    ))
                elif oth.peut_jouer((x, y), joueur, g):
                    ligne.controls.append(ft.Container(
                        content=ft.Column(controls=[ft.Text("🔹", size=20)], expand=True),
                        padding=10,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.GREEN_300,
                        width=50,
                        height=50,
                        ink=True,
                        on_click=lambda e ,x=x ,y=y : jeu_onclick(e,x,y),
                    ))
                else:
                    ligne.controls.append(ft.Container(
                        width=50, height=50,
                        bgcolor=ft.Colors.GREEN_300,
                    ))
            table.controls.append(ligne)

        return table

    
    def jeu_onclick(e, x : int, y: int):
        global coup_joue, joueur
        coup_joue = (x, y)
        jouer_coup()

    def jouer_ia():
        global grille, joueur, g
        start = time.time()
        coup = ia.meilleur_coup(joueur,g,5)

        if coup is None:  #l'IA n'a aucun coup possible
            print(f"L'IA (joueur {joueur}) n'a aucun coup possible, on saute le tour.")
            joueur = oth.autre(joueur)
            grille = generate_grille(joueur, g)
            page.controls[0] = grille
            page.update()
        else:
            g = oth.jouer_coup(coup, joueur, g)
            print(f"Le temps de reflexion de l'ia est de : {time.time() - start}s")
            joueur = oth.autre(joueur)
            grille = generate_grille(joueur, g)
            page.controls[0] = grille
            page.update()

    def jouer_coup():
        global grille, coup_joue, joueur, g
        coups_legaux = oth.coups_possibles(joueur, g)

        if len(coups_legaux) == 0: #l'hum1 n'a aucun coup possible
            print(f"Pas de coups possibles pour le joueur {joueur}, on saute le tour.")
            joueur = oth.autre(joueur)
            grille = generate_grille(joueur, g)
            page.controls[0] = grille
            page.update()
            jouer_ia()

        if coup_joue in coups_legaux:
            g = oth.jouer_coup(coup_joue, joueur, g) # type: ignore
            joueur = oth.autre(joueur)
            grille = generate_grille(joueur, g)
            page.controls[0] = grille
            page.update()
            jouer_ia()

    grille = generate_grille(joueur, g)
    page.add(grille)
    page.update()

ft.app(main)
