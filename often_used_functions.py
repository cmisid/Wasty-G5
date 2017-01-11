# -*- coding: utf-8 -*-
"""
@author: groupe[5]
fichier: often_used_functions.py version 2.0.0
(restructuration: fonction time_between_nodes stockee deplacee dans ce fichier,
 )
"""

import googlemaps
import datetime

# RETRIEVAL_TIME correspond au temps que l'utilisateur passe chez quelqu'un
# le temps de ramasser les dechets (on a choisi 5 min)
RETRIEVAL_TIME = 5
# Coefficient d'importance du temps d'attente par rapport au temps de trajet
# (lorsqu'un utilisateur arrive en avance, son temps d'attente a un poids plus important)
WAITING_FACTOR = 4


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


# RETRIEVAL_TIME correspond au temps que l'utilisateur passe chez quelqu'un
# le temps de ramasser les dechets (on a choisi 5 min)
RETRIEVAL_TIME = 5
# Coefficient d'importance du temps d'attente par rapport au temps de trajet
# (lorsqu'un utilisateur arrive en avance, son temps d'attente a un poids plus important)
WAITING_FACTOR = 2
# Temps maximum d'attente possible a l'arrivee sur un lieu d'une annonce
MAX_WAITING_TIME = 60

"""
ENTREE: time = le temps de depart
        arrival_node = le noeud destination sous la forme suivante
            [coordonnee, debut contrainte horaire, fin contraite horaire, gain]
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
            wait = arrival_node[1] - (time + datetime.timedelta(seconds = duration))
            if wait.seconds/60 > MAX_WAITING_TIME:
                return float("inf")
            else:
                result = datetime.timedelta(seconds = duration) + wait * WAITING_FACTOR
                return (result.seconds/60 + RETRIEVAL_TIME)
    else:
        # Cas de figure 2: il arrive apres la fin de la tranche horaire
        # On lui impose une duree de temps suffisamment penalisante
        # pour l'empecher de passer par ce noeud.
        if arrival_node[2] != None and (time +
            datetime.timedelta(seconds = duration) +
            datetime.timedelta(minutes = RETRIEVAL_TIME)) > arrival_node[2]:
            return float("inf")
        # Cas de figure 3: il arrive a un moment appartenant a la tranche horaire
        # On se retrouve dans ce cas aussi s'il n'y a pas de contrainte horaire
        else:
            return (duration/60 + RETRIEVAL_TIME)