import othello_ia as ia
import time

VIDE = 0
BLANC = 1   # joueur 1
NOIR = 2    # joueur 2

type grille = list[list[int]]
type coup = tuple[int, int]

dico_str_heuristique = {
    0 : "Parité des jetons",
    1 : "Mobilité",
    2 : "Coins",
    3 : "Stabilité",
    4 : "Tableau avec poids",
    5 : "Combinaison des 4 premières"
}

def show(g: grille):
        # Affiche la grille de jeu actuelle en console
        en_joli = {0: "🔸", 1: "⚪", 2: "⚫"}
        coup_inverse = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        print("  1  2  3  4  5  6  7  8  ")
        ligne = ""
        for i in range(8):
            ligne += coup_inverse[i]
            for j in g[i]:
                ligne += en_joli[j] + " "
            print(ligne)
            ligne = ""


def simuler_partie(heuristique_1: int, heuristique_2: int, profondeur: int = 5) -> str:
    start = time.time()
    g = ia.creer_grille()
    joueur = 2
    n_coups = 0

    while not ia.is_game_over(g):
        coups_jouables = ia.coups_possibles(joueur, g)

        if len(coups_jouables) > 0:
            if joueur == 1:
                coup = ia.meilleur_coup(joueur, g, profondeur, heuristique_1)
            else:
                coup = ia.meilleur_coup(joueur, g, profondeur, heuristique_2)
            g = ia.jouer_coup(coup, joueur, g)
            n_coups += 1

        joueur = ia.autre(joueur)

    score = ia.get_score(g)
    if score[0] > score[1]:
        print(f"### LE JOUEUR BLANC ({heuristique_1}) A GAGNÉ avec {dico_str_heuristique[heuristique_1]} contre {dico_str_heuristique[heuristique_2]} ({heuristique_2}) après {n_coups} coups en {time.time() - start:.2f}s ! ###")
        return "blanc"
    elif score[1] > score[0]:
        print(f"### LE JOUEUR NOIR ({heuristique_2}) A GAGNÉ avec {dico_str_heuristique[heuristique_2]} contre {dico_str_heuristique[heuristique_1]} ({heuristique_1}) après {n_coups} coups en {time.time() - start:.2f}s ! ###")
        return "noir"
    else:
        print(f"### MATCH NUL entre {dico_str_heuristique[heuristique_1]} ({heuristique_1}) et {dico_str_heuristique[heuristique_2]} ({heuristique_2}) après {n_coups} coups ###")
        return "nul"
