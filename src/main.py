import flet as ft
from othello import othello as oth
from othello import ia 
import time
import othello_ia as super_ia

grille = ft.Column()
coup_joue = ()
joueur = 2

type_joueur = 2

g = super_ia.creer_grille()

def main(page: ft.Page):
    page.title = "Othello"
    page.window_width = 400 # type: ignore
    page.window_height = 400 # type: ignore
    page.padding = 0
    page.spacing = 10


    score_blanc, score_noir = super_ia.get_score(g)
    scores_text = ft.Text(f"⚪ Joueur 1: {score_blanc} | ⚫ Joueur 2: {score_noir}", size=20)

    def reinitialiser_partie():
        global joueur, g
        joueur = 2
        g = super_ia.creer_grille()

        grille = generate_grille(joueur, g)

        page.controls[0].controls[1].controls[0].controls[0] = grille # type: ignore
        page.update()

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

    grille = generate_grille(joueur, g)

    bouton_reinitialiser = ft.ElevatedButton(
        text="Redémarrer",
        on_click=lambda e: reinitialiser_partie(),
        bgcolor=ft.Colors.RED_500,
        color=ft.Colors.WHITE,
    )

    layout = ft.Row(
        controls=[
            ft.Column(
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls = [grille]
                    ),
                    ft.Row(
                        controls=[scores_text],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[bouton_reinitialiser],
                        alignment=ft.MainAxisAlignment.CENTER,  
                        vertical_alignment=ft.CrossAxisAlignment.CENTER  
                    ),

                ]
            ),
            ft.Column(
                controls = [

                ]
            )
        ]
    )

    page.add(layout)    

    def jeu_onclick(e, x : int, y: int):
        global coup_joue, joueur
        coup_joue = (x, y)
        jouer_coup()

    def jouer_ia():
        global grille, joueur, g
        start = time.time()
        coup = super_ia.meilleur_coup(joueur,g,8,5)

        g = super_ia.jouer_coup(coup, joueur, g) # type: ignore
        print(f"Le temps de reflexion de l'ia est de : {time.time() - start}")
        joueur = super_ia.autre(joueur)
        grille = generate_grille(joueur, g)

        score_blanc, score_noir = super_ia.get_score(g)
        scores_text.value = f"⚪ Joueur 1: {score_blanc} | ⚫ Joueur 2: {score_noir}"
        
        nouvelle_grille = generate_grille(joueur, g)
        page.controls[0].controls[1].controls[0].controls[0] = nouvelle_grille # type: ignore
        page.update()


    def jouer_coup():
        global grille, coup_joue, joueur, g
        g = super_ia.jouer_coup(coup_joue, joueur, g) # type: ignore
        joueur = super_ia.autre(joueur)
        grille = generate_grille(joueur, g)
        score_blanc, score_noir = super_ia.get_score(g)
        scores_text.value = f"⚪ Joueur 1: {score_blanc} | ⚫ Joueur 2: {score_noir}"
        
        nouvelle_grille = generate_grille(joueur, g)
        page.controls[0].controls[1].controls[0].controls[0] = nouvelle_grille # type: ignore
        page.update()
        
        jouer_ia()

    page.update()

ft.app(target=main)
