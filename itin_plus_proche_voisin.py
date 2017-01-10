# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 15:06:40 2017

@author: Groupe[5]
fichier: itin_plus_proche_voisin.py version 1.0.0
"""

import googlemaps

"""
ENTREE: dep_point = le noeud (lieu) de depart
        arv_point = le noeud (lieu) d'arrivee
        mode_transport = le mode de transport
        gmaps = pour utiliser google api avec la bonne cle
OBJECTIF: calcule un arc entre 2 noeuds
SORTIE: retourne un arc sous la forme suivante: 
            [1er noeud, 2eme noeud, distance en metre, duree en secondes]
"""
def calculate_arc(dep_point, arv_point, mode_transport, gmaps):
    distance = gmaps.distance_matrix(dep_point[0], arv_point[0], mode=mode_transport)
    result = [dep_point,
              arv_point,
              distance["rows"][0]["elements"][0]["distance"]["value"],
              distance["rows"][0]["elements"][0]["duration"]["value"]
              ]
    return result


"""
ENTREE: dep_node = noeud de depart
        crossing_points_list = liste des points par lesquels on peut passer
        bool_temps = booleen qui indique si on compare les temps entre 2 points,
            si non, on compare les distances.
OBJECTIF: calcule un itineraire rapidement en cherchant le meilleur noeud
          a partir d'un autre (plus rapide ou plus proche).
SORTIE: retourne un parcours sous la forme d'une liste d'arcs: 
        (un arc: [1er noeud, 2eme noeud, distance en metre, duree en secondes])
"""
def best_itin_nearest_neighbour(dep_node, crossing_points_list, bool_temps):
    gmaps = googlemaps.Client(key='AIzaSyDRpQO4ww7fK610iK5Np-GeiPbCSTuaqec')
    # Nombre de noeuds d'arrivees restants
    nb_elements = len(crossing_points_list)
    itinerary = [dep_node]
    while (nb_elements > 0) :
        # valeur de base d'une distance ou d'un temps minimal
        # qui sera normalement plus grande que n'importe quelle valeur obtenue
        minimum = 1000000
        for i in range (0, len(crossing_points_list)):
            # calcul des distances entre la position de depart et les autres points de passage
            arc = calculate_arc(itinerary[-1],crossing_points_list[i], "driving", gmaps)
            if bool_temps:
                # stockage de la duree qui sera comparee
                value = arc[3]
            else:
                # stockage de la distance qui sera comparee
                value = arc[2]
            if (value < minimum):
                minimum = value
                # on recupere la position de la station la plus proche
                position = arc[1]
        # ajout au chemin
        itinerary.append(position)
        # Reperage du noeud selectionne dans la liste des noeuds potentiels
        index = crossing_points_list.index(position)
        # Supprime le noeud des points de passage possible
        del crossing_points_list[index]
        nb_elements = len(crossing_points_list)
    return itinerary


'''
# Position de depart
dep_node = [(43.6005543, 1.4038282), None, None, 10] #position de depart
# Arrivees possibles
crossing_point=[[(43.620068, 1.435757), None, None, 10],
                [(43.606521, 1.465111), None, None, 10],
                [(43.602729, 1.452065), None, None, 10],
                [(43.612238, 1.427174), None, None, 10]]
crossing_points_list = [[(43.620068, 1.435757), None, None, 10],
                        [(43.606521, 1.465111), None, None, 10],
                        [(43.602729, 1.452065), None, None, 10]
                        ]
bool_temps = False
bool_temps = True
print(best_itin_nearest_neighbour(dep_node, crossing_points_list, bool_temps))
'''