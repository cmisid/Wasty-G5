# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: itin_nearest_neighbour.py version 3.0.0
(ajout: gestion des contraintes horaires, ne tient pas compte des prix)
"""


from often_used_functions import calculate_arc, time_between_nodes
import datetime


"""
ENTREE: dep_node = noeud de depart
        crossing_points_list = liste des points par lesquels on peut passer
        departure_time = moment du depart.
OBJECTIF: calcule un itineraire rapidement en cherchant le meilleur noeud
          a partir d'un autre (plus rapide ou plus proche).
SORTIE: retourne un parcours sous la forme d'une liste de noeuds: 
        (un noeud: [coordonnees GPS (lat/long),
                    heure de debut de la contrainte horaire,
                    heure de fin de la contrainte horaire])
"""
def best_itin_nearest_neighbour(dep_node, crossing_points_list, departure_time):
    # Nombre de noeuds d'arrivees restants
    nb_elements = len(crossing_points_list)
    # Itineraire qui contiendra la liste des noeuds, commence par noeud de depart
    itinerary = [dep_node]
    available_node = True
    basic_minimum = float("inf")
    while (nb_elements > 0) and available_node:
        # valeur de base d'un score minimal
        # qui sera plus grande que n'importe quelle valeur obtenue
        minimum = basic_minimum
        for i in range (0, len(crossing_points_list)):
            # calcul des arcs entre la position de depart et les autres points de passage
            arc = calculate_arc(itinerary[-1],crossing_points_list[i], "driving")
            # stockage de la duree qui sera comparee
            time_value = time_between_nodes(departure_time, crossing_points_list[i], arc[3])
            if (time_value < minimum):
                minimum = time_value
                # on recupere la position de la station la plus proche en terme de score
                position = arc[1]
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
crossing_points_list = [[(43.620068, 1.435757), None, None],
                        [(43.606521, 1.465111), None, None],
                        [(43.602729, 1.452065), None, None],
                        [(43.612238, 1.427174), None, None]
                        ]

dep_time = datetime.datetime.now()
a = dep_time - datetime.timedelta(hours = 2)
b = dep_time - datetime.timedelta(hours = 1)
c = dep_time + datetime.timedelta(hours = 2)
d = dep_time + datetime.timedelta(hours = 3)

crossing_points_list = [[(43.620068, 1.435757), a, b],
                        [(43.606521, 1.465111), a, c],
                        [(43.602729, 1.452065), c, d]
                        ]

print(best_itin_nearest_neighbour(dep_node, crossing_points_list, dep_time))
'''