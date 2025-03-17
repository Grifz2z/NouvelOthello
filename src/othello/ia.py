from . import othello as ot
from math import inf
VIDE = 0
BLANC = 1   # joueur 1
NOIR = 2    # joueur 2

def heuristique(joueur : int, g : ot.grille) -> float:
    grille_comparaison_ = [ [5,-1,3,3,3,3,-1,5],
                            [-1,-1,1,1,1,1,-1,-1],
                            [3,1,2,2,2,2,1,3],
                            [3,1,2,2,2,2,1,3],
                            [3,1,2,2,2,2,1,3],
                            [3,1,2,2,2,2,1,3],
                            [-1,-1,1,1,1,1,-1,-1],
                            [5,-1,3,3,3,3,-1,5],]
    heuri = 0
    print(f"Type de g dans heuristique: {type(g)}, Contenu: {g}")
    scores = ot.get_score(g) #? <-- pb ici, pk ?
    pions_diff = scores[joueur-1] - scores[ot.autre(joueur)-1]
    for i in range(8):
        for j in range(8):
            if g[i][j] == joueur:
                heuri += grille_comparaison_[i][j]
    return heuri**0.5 + pions_diff
        

def grilles_possibles(joueur: int, g: ot.grille) -> list[tuple[ot.grille,ot.coup]]:
    liste_grillecoup = []
    for coup in ot.coups_possibles(joueur,g):
        nouvelle_grile = ot.jouer_coup(coup, joueur,g)
        liste_grillecoup.append((nouvelle_grile, coup))
        
    return liste_grillecoup

def meilleur_coup(joueur: int, g: ot.grille, depth : int)-> ot.coup:
    print("################waza#########################")
    g_possibles = grilles_possibles(joueur=joueur, g=g)
    val_coups_par_minimax = [minimax(depth=depth-1, maximizingPlayer=joueur, g=g_possibles[0][x]) for x in range(len(g_possibles))]
    print(type(g_possibles[1][val_coups_par_minimax.index(max(val_coups_par_minimax))] if joueur-1 else g_possibles[1][val_coups_par_minimax.index(min(val_coups_par_minimax))]))
    print("################################ * WAZA * ###############################################")
    return g_possibles[1][val_coups_par_minimax.index(max(val_coups_par_minimax))] if joueur-1 else g_possibles[1][val_coups_par_minimax.index(min(val_coups_par_minimax))]

def minimax(depth : int, maximizingPlayer: int, g : ot.grille): #Blanc = 1 et Noir = 2
        #L'algorithme MiniMax
        if depth == 0 or ot.is_game_over(g):
            return heuristique(maximizingPlayer, g)
        
        if maximizingPlayer-1:
            maxEval = -inf
            for grille in grilles_possibles(maximizingPlayer,g)[0]:
                evaluation = minimax(depth-1, ot.autre(maximizingPlayer), grille)
                maxEval = max(maxEval, evaluation)
            return maxEval
        else:
            minEval = +inf
            for grille in grilles_possibles(maximizingPlayer,g)[0]:
                evaluation = minimax(depth-1, ot.autre(maximizingPlayer), grille)
                minEval = min(minEval, evaluation)
            return minEval
        
