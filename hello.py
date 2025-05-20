import othello_ia as ia
import time
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
                coup = ia.meilleur_coup(joueur, g, profondeur, heuristique_1, 1)
            else:
                coup = ia.meilleur_coup(joueur, g, profondeur, heuristique_2, 2)
            g = ia.jouer_coup(coup, joueur, g)
            n_coups += 1
            #print(f"Joueur {joueur} a joué {coup} en {time.time() - start:.2f}s")

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

def init_csv_matrix(path: str):
    with open(path, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = [""] + [f"AI {i}" for i in range(6)]
        writer.writerow(header)
        for i in range(6):
            writer.writerow([f"AI {i}"] + ["/" if i == j else "" for j in range(6)])

def maj_csv_resultat(path: str, ligne: int, colonne: int, texte: str):
    with open(path, newline='') as f:
        data = list(csv.reader(f))
    data[ligne + 1][colonne + 1] = texte
    with open(path, 'w', newline='') as f:
        csv.writer(f).writerows(data)

def combats_entre_heuristiques(profondeurs: list[int]):
    heuristiques = list(dico_str_heuristique.keys())

    for profondeur in profondeurs:
        print(f"\n\n========== DÉBUT DES COMBATS À PROFONDEUR {profondeur} ==========\n")
        path_noir = f"resultats_profondeur_{profondeur}_noir.csv"
        path_blanc = f"resultats_profondeur_{profondeur}_blanc.csv"

        init_csv_matrix(path_noir)
        init_csv_matrix(path_blanc)

        for noir in heuristiques:
            for blanc in heuristiques:
                if noir != blanc:
                    gagnant = simuler_partie(heuristique_1=blanc, heuristique_2=noir, profondeur=profondeur)

                    if gagnant == "noir":
                        maj_csv_resultat(path_noir, noir, blanc, "V")  # Noir gagne
                        maj_csv_resultat(path_blanc, blanc, noir, "D") # Blanc perd
                    elif gagnant == "blanc":
                        maj_csv_resultat(path_noir, noir, blanc, "D")  # Noir perd
                        maj_csv_resultat(path_blanc, blanc, noir, "V") # Blanc gagne
                    else:
                        maj_csv_resultat(path_noir, noir, blanc, "N")
                        maj_csv_resultat(path_blanc, blanc, noir, "N")


combats_entre_heuristiques([3])



def heatmap_csv_simple(fichier_csv: str, titre: str):
    with open(fichier_csv, newline='') as f:
        lignes = list(csv.reader(f))

    noms = lignes[0][1:]  # En-têtes
    taille = len(noms)

    data = []
    annotations = []

    for i in range(1, taille + 1):
        ligne_data = []
        ligne_annot = []
        for j in range(1, taille + 1):
            val = lignes[i][j].strip()
            if val == 'V':
                ligne_data.append(1)
            elif val == 'D':
                ligne_data.append(-1)
            else:
                ligne_data.append(0)

            ligne_annot.append(val if val else " ")
        data.append(ligne_data)
        annotations.append(ligne_annot)

    data = np.array(data)

    cmap = sns.color_palette(["#e74c3c", "#f0f0f0", "#2ecc71"])  # rouge, gris, vert
    ax = sns.heatmap(data, annot=annotations, fmt="", xticklabels=noms, yticklabels=noms,
                     cmap=sns.color_palette(["#e74c3c", "#f0f0f0", "#2ecc71"]), center=0, cbar=False, linewidths=0.5, linecolor='gray')

    ax.set_title(titre)
    ax.set_xlabel("Adversaire")
    ax.set_ylabel("IA")
    plt.tight_layout()
    plt.show()


heatmap_csv_simple("resultats_profondeur_5_noir.csv", "IA en NOIR - Profondeur 5")
heatmap_csv_simple("resultats_profondeur_5_blanc.csv", "IA en BLANC - Profondeur 5")
