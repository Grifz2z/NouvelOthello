from typing import List, Tuple

Grille = List[List[int]]
Coup = Tuple[int, int]

def autre(joueur: int) -> int: ...
def poser_pion(c: Coup, joueur: int, g: Grille) -> Grille: ...
def creer_grille() -> Grille: ...
def peut_jouer(c: Coup, joueur: int, g: Grille) -> bool: ...
def coups_possibles(joueur: int, g: Grille) -> List[Coup]: ...
def get_score(g: Grille) -> Tuple[int, int]: ...
def is_game_over(g: Grille) -> bool: ...
def jouer_coup(c: Coup, joueur: int, g: Grille) -> Grille: ...
def meilleur_coup(joueur: int, g: Grille, depth: int, type_heuristique: int, ia: int) -> Coup:
    """
    Calcule le meilleur coup pour un joueur donné en utilisant un algorithme avec une profondeur et une heuristique spécifiées.

    Args:
        joueur (int): Le joueur (1 pour blanc, 2 pour noir).
        g (Grille): La grille représentant l'état actuel du jeu.
        depth (int): La profondeur de recherche de l'algorithme.
        type_heuristique (int): Le type d'heuristique à utiliser :
            - 0 : Parité des jetons.
            - 1 : Mobilité.
            - 2 : Coins.
            - 3 : Stabilité.
            - 4 : Tableau avec poids.
            - 5 : Combinaison des 4 premières.
            - Autre : Aucune heuristique.
        ia (int) : la couleur de l'ia

    Returns:
        Coup: Un tuple représentant les coordonnées du meilleur coup calculé.
    """
    ...
    