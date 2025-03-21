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


def peut_jouer(c: coup, joueur: int, g: grille) -> bool:

    if g[c[0]][c[1]] != 0:
        return False
    
    for dx in range(-1,2):
        for dy in range(-1, 2):
            x = c[0] + dx
            y = c[1] + dy
            encadre = False

            while 0 <= x < 8 and 0 <= y < 8 and g[x][y] == autre(joueur):
                    x += dx
                    y += dy
                    encadre = True
            if 0 <= x < 8 and 0 <= y < 8 and g[x][y] == joueur and encadre:
                    return True
        
    return False


def coups_possibles(joueur: int, g: grille) -> tuple[coup,...]:
    coups = ()
    for x in range(0,8):
        for y in range(0,8):
            c = (x,y)
            if peut_jouer(c, joueur, g):
                coups += (c,)
    return coups

def get_score(g: grille) -> tuple[int, int]:
    score_n = 0
    score_b = 0
    for x in range(0,8):
        for y in range(0,8):
            if g[x][y] == 1:
                score_b += 1
            elif g[x][y] == 2:
                score_n += 1
    return (score_b, score_n)

def jouer_coup(c: coup, joueur: int, g: grille) -> grille:
    nouvelle_grille = [[x for x in g[y]] for y in range(8)]
    if c in coups_possibles(joueur, nouvelle_grille):
        poser_pion(c, joueur, nouvelle_grille)

    for dx in range(-1,2):
        for dy in range(-1, 2):
            x = c[0] + dx
            y = c[1] + dy
            retourner = []

            while 0 <= x < 8 and 0 <= y < 8 and nouvelle_grille[x][y] == autre(joueur):
                retourner.append((x,y))
                x += dx
                y += dy

            if 0 <= x < 8 and 0 <= y < 8 and nouvelle_grille[x][y] == joueur:
                    for flip_x, flip_y in retourner:
                        poser_pion((flip_x, flip_y), joueur, nouvelle_grille)

    return nouvelle_grille



def is_game_over(g: grille) -> bool:
    return len(coups_possibles(1,g))==0 and len(coups_possibles(2,g))==0

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

def partie2j():

    g = creer_grille()
    joueur = 2

    while not is_game_over(g):
        show(joueur, g)
        possibilite_coup_liste = coups_possibles(joueur, g)

        print(f"Coups possibles : {possibilite_coup_liste}")
        coup_joue = input("Quel coup voulez vous jouer ? Si l'on entre 46, c'est qu'on veut jouer le coup (4,6). Coup joué : ")

        while len(coup_joue)!=2 or (int(coup_joue[0]), int(coup_joue[1])) not in possibilite_coup_liste:
            coup_joue = input("Entrée invalide. Coup joué : ")

        coup_joue = (int(coup_joue[0]), int(coup_joue[1]))
        g = jouer_coup(coup_joue, joueur, g)

        joueur = autre(joueur)


    score = get_score(g)
    if score[0]> score[1]:
        print("### LE JOUEUR BLANC A GAGNE ###")
    else:
        print("### LE JOUEUR NOIR A GAGNE ###")
