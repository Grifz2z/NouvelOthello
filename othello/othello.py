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
    coups_dispo = []
    for x in range(8):
        for y in range(8):

            if g[x][y] == joueur:

                for dx in range(-1, 2):
                        for dy in range(-1, 2): 

                            coup_x = x + dx
                            coup_y = y + dy
                            encadre = False

                            while 0 <= coup_x < 8 and 0 <= coup_y < 8 and g[coup_x][coup_y] == autre(joueur):
                                coup_x += dx
                                coup_y += dy
                                encadre = True

                            if 0 <= coup_x < 8 and 0 <= coup_y < 8 and g[coup_x][coup_y] == 0 and encadre:
                                coups_dispo.append((coup_x, coup_y))
    return c in coups_dispo
                            


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

def poser_pion(c: coup, joueur: int, g: grille):
    g[c[0]][c[1]] = joueur

def creer_grille() -> grille:
    """
    Fonction générant la grille de départ du jeu
    """
    g = [[0 for _ in range(8)] for _ in range(8)]

    g[3][3], g[4][4] = 1, 1
    g[4][3], g[3][4] = 2, 2

    return g

show(1, creer_grille())