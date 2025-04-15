from . import othello as ot


VIDE = 0
BLANC = 1   # joueur 1
NOIR = 2    # joueur 2

# ------------------------------------------------------------------------------ Implémentation des heuristiques ----------------------------------------------------------------------------------------

def parite_jeutons(g: ot.grille, joueur: int) -> float:
    """
    Heuristique de parité des pions.
    Renvoie une valeur entre -100 et 100.
    Pour le joueur courant, la formule est :
      100 * (Nombre de pions du joueur - Nombre de pions de l'adversaire)
          / (Nombre de pions du joueur + Nombre de pions de l'adversaire)
    """
    score_blanc = ot.get_score(g)[0]
    score_noir= ot.get_score(g)[1]

    if joueur == BLANC:
        max_coins = score_blanc
        min_coins = score_noir
    else:
        max_coins = score_noir
        min_coins = score_blanc

    if (max_coins + min_coins) != 0:
        return 100 * (max_coins - min_coins) / (max_coins + min_coins)
    else:
        return 0.0


def heuristique_mobilite(g: ot.grille, joueur: int) -> float:
    """
    Heuristique de mobilité (en se basant sur la mobilité actuelle)
    Renvoie une valeur entre -100 et 100 en comparant :
      - le nombre de coups légaux disponibles pour le joueur courant
      - le nombre de coups légaux disponibles pour l'adversaire
    """
    moves_joueur = len(ot.coups_possibles(joueur, g)) # la mobilité est le nb de coups possibles par joueur
    moves_adversaire = len(ot.coups_possibles(ot.autre(joueur), g))
    
    if (moves_joueur + moves_adversaire) != 0:
        return 100 * (moves_joueur - moves_adversaire) / (moves_joueur + moves_adversaire)
    else:
        return 0.0


def heuristique_corners(g: ot.grille, joueur: int) -> float:
    """
    Heuristique des coins capturés.
    Seules les cases (0,0), (0,7), (7,0) et (7,7) sont considérées.
    """
    coins = [(0, 0), (0, 7), (7, 0), (7, 7)]

    valeur_coins_joueur     = 0
    valeur_coins_adversaire = 0

    for i,j in coins:
        if (i,j) in ot.coups_possibles(joueur, g):
            valeur_coins_joueur += 1
        elif (i,j) in ot.coups_possibles(ot.autre(joueur), g):
            valeur_coins_adversaire += 1
        elif g[i][j] == joueur:
            valeur_coins_joueur += 3
        elif g[i][j] == ot.autre(joueur):
            valeur_coins_adversaire += 3


    if (valeur_coins_joueur + valeur_coins_adversaire) !=0:
        return 100 * (valeur_coins_joueur - valeur_coins_adversaire) / (valeur_coins_joueur + valeur_coins_adversaire)
    else: 
        return 0.0



def stable_positions(g: ot.grille) -> set[tuple[int, int]]:
    """
    Renvoie un ensemble de positions sur la grille que l'on peut considérer comme stables,
    en se contentant ici d'une analyse des bords (depuis chaque coin, on balaie la rangée ou
    la colonne tant que les pions sont de même couleur).
    """
    stable = set()
    
    # coin (0,0) en haut à hauche

    if g[0][0]!=0:
        joueur = g[0][0]
        j = 0
        while j<8 and g[0][j] == joueur:
            stable.add((0,j))
            j+=1
        i=0
        while i<8 and g[i][0] == joueur:
            stable.add((i,0))
            i+=1
    
    # coin (0,7) en haut à droite

    if g[0][7]!=0:
        joueur = g[0][7]
        j = 7
        while j>0 and g[0][j] == joueur:
            stable.add((0,j))
            j-=1
        i=0
        while i<8 and g[i][7] == joueur:
            stable.add((i,0))
            i+=1

    # coin (7,0) en bas à gauche

    if g[7][0]!=0:
        joueur = g[7][0]
        j = 0
        while j<8 and g[7][j] == joueur:
            stable.add((0,j))
            j+=1
        i=7
        while i>0 and g[i][0] == joueur:
            stable.add((i,0))
            i-=1

    
    # coin (7,7) en bas à droite

    if g[7][7]!=0:
        joueur = g[7][7]
        j = 7
        while j>0 and g[0][j] == joueur:
            stable.add((0,j))
            j-=1
        i=7
        while i>0 and g[i][7] == joueur:
            stable.add((i,0))
            i-=1

    return stable

def heuristique_stabilite(g: ot.grille, joueur: int) -> float:
    """
    Heuristique de stabilité.
    On calcule, à partir de la fonction 'stable_positions', le nombre de pions stables
    pour le joueur et pour son adversaire, puis on applique la formule :
      100 * (Nombre de pions stables du joueur - Nombre de pions stables de l'adversaire)
          / (Nombre de pions stables du joueur + Nombre de pions stables de l'adversaire)
    """
    places_stabilite = stable_positions(g)
    stable_joueur = sum([1 for (i, j) in places_stabilite if g[i][j] == joueur])
    stable_adversaire = sum([1 for (i, j) in places_stabilite if g[i][j] == ot.autre(joueur)])
    
    if (stable_joueur + stable_adversaire) != 0:
        return 100 * (stable_joueur - stable_adversaire) / (stable_joueur + stable_adversaire)
    else:
        return 0.0

def heuristique_poids_statiques(g: ot.grille, joueur: int)->float:
    """
    Heuristique basé sur un tableau représentant les poids.
    On calcule la difference entre la somme des poids où on 
    trouve les pions du joueur et la somme des poids où on 
    trouve les pions de l'adversaire.
    """
    grille_comparaison_ = [
        [4, -3, 2, 2, 2, 2, -3, 4],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [4, -3, 2, 2, 2, 2, -3, 4]
                        ]
    utilite_joueur = 0
    utilite_adversaire = 0

    for i in range(8):
        for j in range(8):
            if g[i][j] == joueur:
                utilite_joueur += grille_comparaison_[i][j]
            elif g[i][j] == ot.autre(joueur):
                utilite_adversaire += grille_comparaison_[i][j]

    return utilite_joueur-utilite_adversaire
