# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: score.py version 2.0.0
(restructuration: fonction calculate_path stockee dans un autre fichier,
 correction: gestion de l'heure de depart dans shortest_path)
"""

import itertools
import datetime

from often_used_functions import calculate_path


# RETRIEVAL_TIME correspond au temps que l'utilisateur passe chez quelqu'un
# le temps de ramasser les dechets (on a choisi 5 min)
RETRIEVAL_TIME = 5

# Coefficient d'importance du temps d'attente par rapport au temps de trajet
# (lorsqu'un utilisateur arrive en avance, son temps d'attente a un poids plus important)
WAITING_FACTOR = 4

# Coefficients d'importance des parametres pour calculer le score d'un parcours.
# Fortement susceptibles de changer.
DURATION_FACTOR = 0.33 #importance de la duree du trajet
PRICE_FACTOR = 1 #importance du gain


"""
ENTREE: time = le temps de depart
        arrival_node = le noeud destination sous la forme suivante
            [coordonnee, debut contrainte horraire, fin contraite horraire, gain]
        duration = la duree du trajet entre le depart et la destination, en s
OBJECTIF: donner le temps du trajet avec le possible temps d'attente
SORTIE: la duree totale en minute
"""
def time_between_nodes(time, arrival_node, duration):
    # Cas de figure 1: l'utilisateur arrive avant le debut de la tranche horaire
    # On impose a l'utilisateur d'attendre jusqu'au debut de cette tranche
    if arrival_node[1] != None and (time +
        datetime.timedelta(seconds = duration) + 
        datetime.timedelta(minutes = RETRIEVAL_TIME) < arrival_node[1]):
        result = arrival_node[1] - time
        result = datetime.timedelta(seconds = duration) + (
            arrival_node[1] - (time + datetime.timedelta(seconds = duration))
            ) * WAITING_FACTOR
        return (result.total_seconds()/60 + RETRIEVAL_TIME)
    else:
        # Cas de figure 2: il arrive apres la fin de la tranche horaire
        # On lui impose une duree de temps suffisamment penalisante
        # pour l'empecher de passer par ce noeud.
        if arrival_node[2] != None and (time +
            datetime.timedelta(seconds = duration) +
            datetime.timedelta(minutes = RETRIEVAL_TIME)) > arrival_node[2]:
            return 100000
        # Cas de figure 3: il arrive a un moment appartenant a la tranche horaire
        # On se retrouve dans ce cas aussi s'il n'y a pas de contrainte horaire
        else:
            return (duration/60 + RETRIEVAL_TIME)


"""
ENTREE: node = tous les noeuds sous forme de liste
        departure = la date et heure de depart du premier noeud
OBJECTIF: calcule le parcours le plus avantageux
SORTIE: la liste des noeuds dans le meilleur ordre
"""
def shortest_path(nodes, departure_time):
    score = 0
    time = 0
    has_best_path = False
    result = []
    # local_dep_time correspond au moment de depart du noeud sur lequel on se trouve.
    local_dep_time = departure_time
    # path_list correspond a l'ensemble des chemins pour chaque paire de noeud.
    path_list = calculate_path(nodes, "driving")
    # On essaie tous les nombres de noeuds possibles.
    for nb_nodes in range(2,len(nodes) + 1):
        # On passe par toutes les combinaisons possibles
        for subset in itertools.permutations(nodes, nb_nodes):
            if (subset[0] == nodes[0]):
                i = 0
                # On calcule le score pour chaque trajet, a partir du temps et du prix,
                # en mettant un coefficient discriminant devant chacun des parametres,
                # et on calcule la somme des scores de tous les trajets.
                # Si on obtient un temps superieur a 100000, le parcours ne sera pas interessant.
                while (time < 100000) and i < (len(subset) - 1):
                    j = 0
                    while (time < 100000) and j <(len(path_list)):
                        if path_list[j][0] == subset[i] and path_list[j][1] == subset[i + 1]:
                            time = time_between_nodes(local_dep_time, subset[i + 1] , path_list[j][3])                        
                            local_dep_time = local_dep_time + datetime.timedelta(minutes = time)
                            score = score + (DURATION_FACTOR * time - PRICE_FACTOR * subset[i + 1][3])
                        j = j + 1
                    i = i + 1
                full_score = score
                if not has_best_path :
                    min_score = full_score
                    has_best_path = True
                    result = subset
                else:
                    if(min_score > full_score):
                        min_score = full_score
                        result = subset
                score = 0
                local_dep_time = departure_time
    return result

'''
# Test pour les horaires (heure de depart, contraintes horaires debut et fin)
dep = datetime.datetime(2017,1,16,11,30,0)
a = datetime.datetime(2017,1,16,12,0,0)
b = datetime.datetime(2017,1,16,14,0,0)

# Ensemble de noeud test
# Un noeud comprend :
#   - des coordonnees GPS (latitude/longitude)
#   - le debut de la contraite horaire du donneur (type datetime.datetime)
#   - la fin de la contraite horaire du donneur (type datetime.datetime)
#   - un prix (paye pour le recyclage).
test_noeud = [[(43.6005543,1.4038282),  None, None,  0],
              [ (43.620068, 1.435757),     a,    b, 10],
              [ (43.606521, 1.465111),  None, None, 10],
              [ (43.602729, 1.452065),  None, None,  0],
              [ (43.612238, 1.427174),  None, None,  0]
              ]

test_noeud = [[(43.6005543,1.4038282),  None, None,  0],
              [ (43.620068, 1.435757),     a,    b,  5],
              [ (43.606521, 1.465111),  None, None, 10],
              ]

# Appel a la fonction.
print(shortest_path(test_noeud, dep))
'''