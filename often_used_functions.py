# -*- coding: utf-8 -*-
"""
@author: groupe[5]
fichier: often_used_functions.py version 1.0.0
"""

import googlemaps

"""
ENTREE: dep_point = le noeud (lieu) de depart
        arv_point = le noeud (lieu) d'arrivee
        mode_transport = le mode de transport
OBJECTIF: calcule un arc entre 2 noeuds
SORTIE: retourne un arc sous la forme suivante:
            [1er noeud, 2eme noeud, distance en metre, duree en secondes]
"""
def calculate_arc(dep_point, arv_point, mode_transport):
    # pour utiliser google api avec la bonne cle
    gmaps = googlemaps.Client(key='AIzaSyDRpQO4ww7fK610iK5Np-GeiPbCSTuaqec')
    distance = gmaps.distance_matrix(dep_point[0], arv_point[0], mode=mode_transport)
    result = [dep_point,
              arv_point,
              distance["rows"][0]["elements"][0]["distance"]["value"],
              distance["rows"][0]["elements"][0]["duration"]["value"]
              ]
    return result


"""
ENTREE: node = tous les noeuds sous forme de liste
        mode_transport = le mode de transport
OBJECTIF: calcule tous les arcs entre pour chaque couple de noeud
SORTIE: retoure une liste d'arc sous la forme suivante:
            [1er noeud, 2eme noeud, distance en metre, duree en secondes]
"""
def calculate_path(nodes, mode_transport):
    path = []
    for i in nodes:
        for j in nodes:
            if (j != i) :
                path.append(calculate_arc(i, j, mode_transport))
    return path