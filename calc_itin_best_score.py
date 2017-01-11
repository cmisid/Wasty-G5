# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: score.py version 3.0.0
(restructuration: fonction time_between_nodes stockee dans un autre fichier,
 suppression, ne tient pas compte du prix)
"""

import itertools
import datetime

from often_used_functions import calculate_path, time_between_nodes


"""
ENTREE: node = tous les noeuds sous forme de liste
        departure = la date et heure de depart du premier noeud
OBJECTIF: calcule le parcours le plus avantageux
SORTIE: la liste des noeuds dans le meilleur ordre
"""
def shortest_path(nodes, departure_time):
    score = 0
    local_dep_time = departure_time
    result = []
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
                            time = time_between_nodes(local_dep_time, subset[i + 1] , path_list[j][3])
                            local_dep_time = local_dep_time + datetime.timedelta(minutes = time)
                            if time != float("inf"):
                                score = score + time
                            else:
                                score = float("inf")
                        j = j + 1
                    i = i + 1
                if(min_score > score):
                    min_score = score
                    result = subset
                score = 0
                local_dep_time = departure_time
        opt_nb_node = (min_score != float("inf"))
        nb_nodes = nb_nodes - 1
    return result



# Test pour les horaires (heure de depart, contraintes horaires debut et fin)
dep = datetime.datetime(2017,1,16,11,30,0)
a = datetime.datetime(2017,1,16,12,0,0)
b = datetime.datetime(2017,1,16,14,0,0)

# Ensemble de noeud test
# Un noeud comprend :
#   - des coordonnees GPS (latitude/longitude)
#   - le debut de la contraite horaire du donneur (type datetime.datetime)
#   - la fin de la contraite horaire du donneur (type datetime.datetime)
test_noeud = [[(43.6005543,1.4038282),  None, None],
              [ (43.620068, 1.435757),     a,    b],
              [ (43.606521, 1.465111),  None, None],
              [ (43.602729, 1.452065),  None, None],
              [ (43.612238, 1.427174),  None, None]
              ]

test_noeud = [[(43.6005543,1.4038282),  None, None],
              [ (43.620068, 1.435757),     a,    b],
              [ (43.606521, 1.465111),  None, None],
              ]

# Appel a la fonction.
print(shortest_path(test_noeud, dep))
