# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: calc_itin_best_score.py version 4.0.0
(ajout: gestion de la capacite max)
"""

import itertools
import datetime

from often_used_functions import calculate_path, time_between_nodes
from capacity import estimate_capacity


"""
ENTREE: node = tous les noeuds sous forme de liste
        departure_time = la date et heure de depart du premier noeud
        car_size = taille du vehicule
OBJECTIF: calcule le parcours le plus avantageux
SORTIE: la liste des noeuds dans le meilleur ordre
"""
def shortest_path(nodes, departure_time, car_size):
    # Initialisation des variables locales
    score = 0
    local_dep_time = departure_time
    result = []
    current_weight = 0
    current_volume = 0
    # path_list correspond a l'ensemble des chemins pour chaque paire de noeud.
    path_list = calculate_path(nodes, "driving")
    opt_nb_node = False
    nb_nodes = len(nodes)
    min_score = float("inf")
    
    # On essaie tous les nombres de noeuds possibles.
    #for nb_nodes in range(1,len(nodes) + 1):
    while not (opt_nb_node):
        # On passe par toutes les combinaisons possibles, en commencant par
        # celles qui contiennent le plus de noeud pour maximiser la recolte,
        # puis en enlevant 1 a chaque fois.
        for subset in itertools.permutations(nodes, nb_nodes):
            if(subset[0] == nodes[0]):
                i = 0
                # On calcule un score base sur le temps pour chaque trajet,
                # et on calcule la somme des scores de tous les trajets.
                # Si on obtient un temps infini, le parcours ne sera pas interessant.
                while (score < float("inf")) and i < (len(subset) - 1):
                    j = 0
                    while (score < float("inf")) and j <(len(path_list)):
                        if path_list[j][0] == subset[i] and path_list[j][1] == subset[i + 1]:
                            # On ne gere pas les contraintes de capacite si la
                            # taille de la voiture n'est pas bien renseignee
                            if car_size != None:
                                current_weight, current_volume = estimate_capacity(
                                    car_size, current_weight, current_volume, subset[i + 1]
                                )
                            time = time_between_nodes(local_dep_time, subset[i + 1] , path_list[j][3])
                            local_dep_time = local_dep_time + datetime.timedelta(minutes = time)
                            # On inflige un score infini si une contrainte horaire
                            # ou de capacite n'esr pas bien respectee
                            if current_weight != float("inf"
                                ) and current_volume != float("inf"
                                ) and time != float("inf"):
                                score = score + time
                            else:
                                score = float("inf")
                        j = j + 1
                    i = i + 1
                if(min_score > score):
                    min_score = score
                    result = subset
                # Reinitialisation des variables locales
                score = 0
                local_dep_time = departure_time
                current_weight = 0
                current_volume = 0
        opt_nb_node = (min_score != float("inf"))
        nb_nodes = nb_nodes - 1
    return result


'''
# Test pour les horaires (heure de depart, contraintes horaires debut et fin, taille vehicule)
dep = datetime.datetime(2017,1,16,11,30,0)
a = datetime.datetime(2017,1,16,12,0,0)
b = datetime.datetime(2017,1,16,14,0,0)
car_size = "moyen"

# Ensemble de noeud test
# Un noeud comprend :
#   - des coordonnees GPS (latitude/longitude)
#   - le debut de la contraite horaire du donneur (type datetime.datetime)
#   - la fin de la contraite horaire du donneur (type datetime.datetime)
#   - le poids approximatif de(s)/l' objet(s) recupere(s)
#   - le volume approximatif de(s)/l' objet(s) recupere(s)
test_noeud = [[(43.6005543,1.4038282),  None, None, None, None],
              [ (43.620068, 1.435757),     a,    b,  100,    1],
              [ (43.606521, 1.465111),  None, None,   20,    1],
              [ (43.602729, 1.452065),  None, None,  500,    8],
              [ (43.612238, 1.427174),  None, None,  300,    3]
              ]

test_noeud = [[(43.6005543,1.4038282),  None, None, None, None],
              [ (43.620068, 1.435757),     a,    b,  200,    3],
              [ (43.606521, 1.465111),  None, None,  700,    8],
              ]
print(shortest_path(test_noeud, dep, car_size))

test_noeud = [[(43.6005543,1.4038282),  None, None, None, None],
              [ (43.620068, 1.435757),     a,    b,  200,    3],
              [ (43.606521, 1.465111),  None, None,  900,    8],
              ]
print(shortest_path(test_noeud, dep, car_size))

test_noeud = [[(43.6005543,1.4038282),  None, None, None, None],
              [ (43.620068, 1.435757),     a,    b,  200,    3],
              [ (43.606521, 1.465111),  None, None,  100,    1],
              ]
print(shortest_path(test_noeud, dep, car_size))
'''