VIDE = 0
BLANC = 1   # joueur 1
NOIR = 2    # joueur 2

type grille = list[list[int]]
type coup = tuple[int, int]

def autre(joueur: int) -> int:
    """
    Retourne l'autre joueur
    """
    assert joueur in (1,2), "Seuls les joueurs 1 et 2 sont possibles"
    return 3-joueur

def peut_jouer(c: coup, joueur: int, g: grille) -> bool:
    """Cette fonction a besoin d'exister pour l'affichage.
    Vous l'écrirez en chemin """
    return False

def show(joueur: int, g: grille):
    """
    Affiche la grille g, le joueur allant jouer étant donné
    """
    print( "".join(f"   {j}" for j in range(8)))
    print(" ┌───"+ 7*"┬───" +"┐")
    for i in range(8):
        print(f"{i}│", end="")
        for j in range(8):
            if g[i][j]==NOIR:
                print(" ○ ", end="│")
            elif g[i][j]==BLANC:
                print(" ● ", end="│")
            elif peut_jouer((i,j), joueur, g):
                print(" . ", end="│")
            else:
                print("   ", end="│")
        print()
        if i == 7:
            print(" └───"+ 7*"┴───" +"┘")
        else:
            print(" ├───"+ 7*"┼───" +"┤")
    print(f"C'est le tour du joueur {joueur}")

