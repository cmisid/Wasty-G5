# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: itin_nearest_neighbour.py version 4.0.0
(ajout: gestion de la capacite maximale)
"""


from often_used_functions import calculate_arc, time_between_nodes
from capacity import estimate_capacity

import datetime


"""
ENTREE: dep_node = noeud de depart
        crossing_points_list = liste des points par lesquels on peut passer
        departure_time = moment du depart
        car_size = taille du vehicule
OBJECTIF: calcule un itineraire rapidement en cherchant le meilleur noeud
          a partir d'un autre (plus rapide ou plus proche).
SORTIE: retourne un parcours sous la forme d'une liste de noeuds: 
        (un noeud: [coordonnees GPS (lat/long),
                    heure de debut de la contrainte horaire,
                    heure de fin de la contrainte horaire,
                    le poids approximatif,
                    le volume approximatif])
"""
def best_itin_nearest_neighbour(dep_node, crossing_points_list, departure_time, car_size):
    # Nombre de noeuds d'arrivees restants
    nb_elements = len(crossing_points_list)
    # Itineraire qui contiendra la liste des noeuds, commence par noeud de depart
    itinerary = [dep_node]
    available_node = True
    basic_minimum = float("inf")
    # Gestion ou non de la capacite maximale
    if car_size != None:
        current_weight = 0
        current_volume = 0
        manage_cap = True
    else:
        manage_cap = False
    while (nb_elements > 0) and available_node:
        # valeur de base d'un score minimal
        # qui sera plus grande que n'importe quelle valeur obtenue
        minimum = basic_minimum
        for i in range (0, len(crossing_points_list)):
            # calcul des arcs entre la position de depart et les autres points de passage
            arc = calculate_arc(itinerary[-1],crossing_points_list[i], "driving")
            # stockage de la duree qui sera comparee
            time_value = time_between_nodes(departure_time, crossing_points_list[i], arc[3])
            # Gestion ou non de la capacite max une fois qu'on a trouve un meilleur score temps
            if time_value < minimum and not manage_cap:
                minimum = time_value
                # on recupere la position de la station la plus proche en terme de score
                position = arc[1]
            elif time_value < minimum and manage_cap:
                cum_weight, cum_volume = estimate_capacity(
                    car_size, current_weight, current_volume, crossing_points_list[i]
                )
                # verification que la capacite max n'est pas depassee
                if float("inf") not in (cum_weight, cum_volume):
                    minimum = time_value
                    # on recupere la position de la station la plus proche en terme de score
                    position = arc[1]
                    # mise a jour du poids et du volume contenu
        current_weight, current_volume = cum_weight, cum_volume
        if minimum != basic_minimum:
            # ajout au chemin
            itinerary.append(position)
            # mise a jour du temps
            departure_time = departure_time + datetime.timedelta(minutes = minimum)
            # Reperage du noeud selectionne dans la liste des noeuds potentiels
            index = crossing_points_list.index(position)
            # Supprime le noeud des points de passage possible
            del crossing_points_list[index]
            nb_elements = len(crossing_points_list)
        else:
            # Dans ce cas, on stoppe notre parcours et on n'ajoute pas
            # de noeud à l'itineraire
            available_node = False
    return itinerary


'''
# Position de depart
dep_node = [(43.6005543, 1.4038282), None, None]
# Arrivees possibles
crossing_points_list = [[(43.620068, 1.435757), None, None, None, None],
                        [(43.606521, 1.465111), None, None, None, None],
                        [(43.602729, 1.452065), None, None, None, None],
                        [(43.612238, 1.427174), None, None, None, None]
                        ]

dep_time = datetime.datetime.now()
car_size = "moyen"
a = dep_time - datetime.timedelta(hours = 2)
b = dep_time - datetime.timedelta(hours = 1)
c = dep_time + datetime.timedelta(hours = 2)
d = dep_time + datetime.timedelta(hours = 3)

crossing_points_list = [[(43.620068, 1.435757), a, b, 100, 1],
                        [(43.606521, 1.465111), a, c, 200, 3],
                        [(43.602729, 1.452065), c, d, 400, 3],
                        [(43.612238, 1.427174), b, d, 900, 8],
                        ]

print(best_itin_nearest_neighbour(dep_node, crossing_points_list, dep_time, car_size))
'''