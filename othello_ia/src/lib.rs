use std::collections::HashSet;
use std::f32::INFINITY;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::PyList;

pub type Grille = [[u8; 8]; 8];
pub type Coup = (usize, usize);

// ------------------------------------------------------------------------------ Othello ----------------------------------------------------------------------------------------


#[pyfunction]
fn autre(joueur: u8)-> PyResult<u8> {
    match joueur {
        1 => Ok(2),
        2 => Ok(1),
        _ => Err(pyo3::exceptions::PyValueError::new_err("Seuls les joueurs 1 (BLANC) et 2 (NOIR) sont valides"))
    }
}

fn autre_interne(joueur: u8) -> u8 {
    return 3 - joueur
}

fn poser_pion_interne(c: Coup, joueur: u8, mut g: Grille) -> Grille {
    g[c.0][c.1] = joueur;
    g
}

#[pyfunction]
fn poser_pion(c: Coup, joueur: u8, g: Grille) -> Grille {
    poser_pion_interne(c, joueur, g)
}

#[pyfunction]
fn creer_grille() -> Grille {
    let mut g: Grille = [[0; 8]; 8];
    g[3][3] = 1;
    g[4][4] = 1;
    g[4][3] = 2;
    g[3][4] = 2;
    return g
}

fn dans_grille(x: isize, y: isize) -> bool {
    x >= 0 && x < 8 && y >= 0 && y < 8
}

fn peut_jouer_interne(c: Coup, joueur: u8, g:Grille)-> bool {
    if g[c.0][c.1] != 0 {
        return false;
    }

    for dx in -1..=1  {
        for dy in -1..=1 {
            let mut x = c.0 as isize + dx;
            let mut y = c.1 as isize + dy;
            let mut encadre = false;

            while dans_grille(x, y) && g[x as usize][y as usize] == autre_interne(joueur) {
                x += dx;
                y += dy;
                encadre = true
            };
            if dans_grille(x, y) && g[x as usize][y as usize] == joueur && encadre {
                return true;
            }
        }
    }
    return false;
}

#[pyfunction]
fn peut_jouer(c: Coup, joueur: u8, g:Grille)-> PyResult<bool> {
    return Ok(peut_jouer_interne(c, joueur, g));
}


fn coups_possibles_interne(joueur: u8, g:Grille)-> Vec<Coup> {
    let mut coups = Vec::new();
    for x in 0..8 {
        for y in 0..8{
            let c: Coup = (x,y);
            if peut_jouer_interne(c, joueur, g) {
                coups.push(c)
            }
        }
    }
    return coups;
}

#[pyfunction]
fn coups_possibles(joueur: u8, g:Grille)-> PyResult<Vec<Coup>> {
    return Ok(coups_possibles_interne(joueur, g));
}

fn get_score_interne(g: Grille)-> (u8, u8) {
    let mut score_blanc :u8 = 0;
    let mut score_noir :u8 = 0;
    for x in 0..8 {
        for y in 0..8 {
            match g[x][y] {
                1 => score_blanc += 1,
                2 => score_noir += 1,
                _ => (),
            }
        }
    }
    return (score_noir, score_blanc);
}

#[pyfunction]
fn get_score(g: Grille)-> PyResult<(u8, u8)> {
    return Ok(get_score_interne(g));
}

fn is_game_over_interne(g: Grille) -> bool {
    return coups_possibles_interne(1, g).is_empty() && coups_possibles_interne(2, g).is_empty()
}

#[pyfunction]
fn is_game_over(g:Grille)-> PyResult<bool> {
    return Ok(is_game_over_interne(g));
}

fn jouer_coup_interne(c: Coup, joueur: u8, g: Grille) -> Grille {
    if !peut_jouer_interne(c, joueur, g) {
        return g;
    }

    let mut nouvelle_grille = poser_pion_interne(c, joueur, g);

    for dx in -1..=1 {
        for dy in -1..=1 {
            if dx == 0 && dy == 0 { continue; }
            let mut x = c.0 as isize + dx;
            let mut y = c.1 as isize + dy;
            let mut retourner = Vec::new();

            while dans_grille(x, y) && g[x as usize][y as usize] == autre_interne(joueur) {
                retourner.push((x as usize, y as usize));
                x += dx;
                y += dy;
            }

            if dans_grille(x, y) && g[x as usize][y as usize] == joueur {
                for (flip_x, flip_y) in retourner {
                    nouvelle_grille[flip_x][flip_y] = joueur;
                }
            }
        }
    };
    return nouvelle_grille;
}

#[pyfunction]
fn jouer_coup(c: Coup, joueur: u8, g:Grille)-> PyResult<Grille> {
    return Ok(jouer_coup_interne(c, joueur, g));
}

// ------------------------------------------------------------------------------ Implémentation des heuristiques ----------------------------------------------------------------------------------------


fn parite_jetons(g: Grille, joueur: u8) -> f32 {
    let (score_noir, score_blanc) = get_score_interne(g);

    let (max_coins, min_coins) = if joueur == 1 {
        (score_blanc as f32, score_noir as f32)
    } else {
        (score_noir as f32, score_blanc as f32)
    };

    if (max_coins + min_coins) != 0.0 {
        100.0 * (max_coins - min_coins) / (max_coins + min_coins)
    } else {
        0.0
    }
}

fn heuristique_mobilite(g: Grille, joueur: u8) -> f32 {
    let nb_coups_joueur: f32 = coups_possibles_interne(joueur, g).len() as f32;
    let nb_coups_adversaire: f32 = coups_possibles_interne(autre_interne(joueur), g).len() as f32;

    if (nb_coups_joueur + nb_coups_adversaire) != 0.0 {
        return 100.0 *(nb_coups_joueur - nb_coups_adversaire)/(nb_coups_joueur + nb_coups_adversaire);
    } else {
        return 0.0;
    }
}

fn heuristique_coins(g: Grille , joueur: u8) -> f32 {
    let corners = [(0, 0), (0, 7), (7, 0), (7, 7)];
    let mut coins_jou : f32 = 0.0;
    let mut coins_adv : f32 = 0.0;


    for &(x, y) in &corners {
        if g[x][y] == joueur {
            coins_jou += 25.0;
        } else if g[x][y] == autre_interne(joueur) {
            coins_adv += 25.0;
        }
    }

    if (coins_jou + coins_adv) != 0.0 {
        return 100.0 *(coins_jou - coins_adv)/(coins_jou + coins_adv);
    } else {
        return 0.0;
    }

}

fn positions_stables(g: &Grille) -> HashSet<(usize, usize)> {
    let mut stable = HashSet::new();

    // Coin (0,0) en haut à gauche
    if g[0][0] != 0 {
        let joueur = g[0][0];
        let mut j = 0;
        while j < 8 && g[0][j] == joueur {
            stable.insert((0, j));
            j += 1;
        }
        let mut i = 0;
        while i < 8 && g[i][0] == joueur {
            stable.insert((i, 0));
            i += 1;
        }
    }

    // Coin (0,7) en haut à droite
    if g[0][7] != 0 {
        let joueur = g[0][7];
        let mut j = 7;
        while j > 0 && g[0][j] == joueur {
            stable.insert((0, j));
            j -= 1;
        }
        let mut i = 0;
        while i < 8 && g[i][7] == joueur {
            stable.insert((i, 7));
            i += 1;
        }
    }

    // Coin (7,0) en bas à gauche
    if g[7][0] != 0 {
        let joueur = g[7][0];
        let mut j = 0;
        while j < 8 && g[7][j] == joueur {
            stable.insert((7, j));
            j += 1;
        }
        let mut i = 7;
        while i > 0 && g[i][0] == joueur {
            stable.insert((i, 0));
            i -= 1;
        }
    }

    // Coin (7,7) en bas à droite
    if g[7][7] != 0 {
        let joueur = g[7][7];
        let mut j = 7;
        while j > 0 && g[7][j] == joueur {
            stable.insert((7, j));
            j -= 1;
        }
        let mut i = 7;
        while i > 0 && g[i][7] == joueur {
            stable.insert((i, 7));
            i -= 1;
        }
    }

    stable
}

fn heuristique_stabilite(g: &Grille, joueur: u8) -> f32 {
    let places_stabilite = positions_stables(g);
    let stable_joueur = places_stabilite.iter().filter(|&&(i, j)| g[i][j] == joueur).count();
    let stable_adversaire = places_stabilite.iter().filter(|&&(i, j)| g[i][j] == autre_interne(joueur)).count();

    if (stable_joueur + stable_adversaire) != 0 {
        100.0 * (stable_joueur as f32 - stable_adversaire as f32) / (stable_joueur as f32 + stable_adversaire as f32)
    } else {
        0.0
    }
}

fn heuristique_poids_statiques(g: Grille, joueur: u8)-> f32 {
    let grille_comparaison_ = [
        [4, -3, 2, 2, 2, 2, -3, 4],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [4, -3, 2, 2, 2, 2, -3, 4]
                        ];

    let mut utilite_jou: f32 = 0.0;
    let mut utilite_adv: f32 = 0.0;

    for i in 0..8 {
        for j in 0..8 {
            if g[i][j] == joueur {
                utilite_jou += grille_comparaison_[i][j] as f32
            } else if g[i][j] == autre_interne(joueur) {
                utilite_adv += grille_comparaison_[i][j] as f32
            }
        }
    }

    return utilite_jou - utilite_adv;
}

// ------------------------------------------------------------------------------ IA ----------------------------------------------------------------------------------------

fn heuristique(joueur: u8, g: Grille) -> f32 {
    return parite_jetons(g, joueur);
}

fn grilles_possibles(joueur: u8, g:Grille)-> Vec<(Grille,Coup)> {
    let mut liste_grillecoup: Vec<(Grille,Coup)> = Vec::new();

    for coup in coups_possibles_interne(joueur, g) {
        let new_grille = jouer_coup_interne(coup, joueur, g);
        liste_grillecoup.push((new_grille, coup));
    };

    return liste_grillecoup;
}

fn minimax(depth : u8, maximizing_player: u8, g: Grille) -> f32 {
    if depth == 0 || is_game_over_interne(g) {
        return heuristique(maximizing_player, g);
    }
    else if maximizing_player == 2 {
        let mut max_eval = -INFINITY;
        for (grille, _) in grilles_possibles(maximizing_player, g).iter() {
            let evaluation = minimax(depth-1, autre_interne(maximizing_player), *grille);
            max_eval = max_eval.max( evaluation)
        };
        return max_eval;
    }
    else{
        let mut min_eval = INFINITY;
        for (grille, _) in grilles_possibles(maximizing_player, g).iter() {
            let evaluation = minimax(depth-1, autre_interne(maximizing_player), *grille);
            min_eval = min_eval.min(evaluation)
        };
        return min_eval;
    }
}

//def alpha_beta(depth : u8, maximizing_player: u8, g: Grille, α : f32, β : f32) -> f32 {
//    if depth == 0 || is_game_over_interne(g) {
//        return heuristique(maximizing_player, g);
//    }
//    else if maximizing_player == 2 {
//        let mut max_eval = -INFINITY;
//        for (grille, _) in grilles_possibles(maximizing_player, g).iter() {
//            let evaluation = minimax(depth-1, autre_interne(maximizing_player), *grille);
//            max_eval = max_eval.max( evaluation)
//        };
//        return max_eval;
//    }
//    else{
//        let mut min_eval = INFINITY;
//        for (grille, _) in grilles_possibles(maximizing_player, g).iter() {
//            let evaluation = minimax(depth-1, autre_interne(maximizing_player), *grille);
//            min_eval = min_eval.min(evaluation)
//        };
//        return min_eval;
//    }
//}

fn meilleur_coup_interne(joueur: u8, g: Grille, depth: u8) -> Coup {
    let mut best_score = -INFINITY;
    let mut best_coup = (0, 0);

    for (grille, coup) in grilles_possibles(joueur, g) {
        let score = minimax(depth - 1, autre_interne(joueur), grille);
        if score > best_score {
            best_score = score;
            best_coup = coup;
        }
    }
    best_coup
}



#[pyfunction]
fn meilleur_coup(joueur: u8, g: Grille, depth: u8) -> PyResult<Coup> {
    return Ok(meilleur_coup_interne(joueur, g, depth));
}

#[pymodule]
fn othello_ia(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(autre, module)?)?;
    module.add_function(wrap_pyfunction!(poser_pion, module)?)?;
    module.add_function(wrap_pyfunction!(creer_grille, module)?)?;
    module.add_function(wrap_pyfunction!(peut_jouer, module)?)?;
    module.add_function(wrap_pyfunction!(coups_possibles, module)?)?;
    module.add_function(wrap_pyfunction!(get_score, module)?)?;
    module.add_function(wrap_pyfunction!(is_game_over, module)?)?;
    module.add_function(wrap_pyfunction!(jouer_coup, module)?)?;
    module.add_function(wrap_pyfunction!(meilleur_coup, module)?)?;

    Ok(())
}