# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: manage_json.py version 2.0.0
(ajout: gestion du poids et du volume pour la capacite maximale)
"""

import datetime
from often_used_functions import RETRIEVAL_TIME
from capacity import convert_volume


"""
ENTREE: un string sous la forme H:M:S
OBJECTIF: convertit un string en datetime
SORTIE: un datetime
"""
def string_to_datetime(string_time):
    time = datetime.datetime.strptime(string_time, '%H:%M:%S').time()
    date = datetime.datetime.now()
    return datetime.datetime.combine(date,time)


"""
ENTREE: un noeud
OBJECTIF: fait en sorte d'avoir le debut d'une plage horaire avant la fin
SORTIE: le noeud potentiellement corrige
"""
def verif_datetime(node):
    # On autorise minuit comme heure de fin
    if node[1] > node[2] and node[2].time() != datetime.time(0, 0, 0):
        node[1], node[2] = node[2], node[1]
    if node[2].time() == datetime.time(0, 0, 0):
        node[2] = node[2] + datetime.timedelta(days = 1)
    # Pour un meilleur fonctionnement, il faut qu'on ait un intervalle
    # qui soit d'une longueur superieure ou egale au temps de recuperation
    if ((node[2] - node[1]).seconds / 60) < RETRIEVAL_TIME:
        node[2] = node[1] + datetime.timedelta(minutes = 5)
    return node


"""
ENTREE: le contenu d'un fichier json contenant les donnees necessaires
    a l'execution de notre calcul de meilleur parcours
OBJECTIF: renvoyer les donnees necessaires a l'execution du calcul de meilleur parcours
SORTIE: une liste des donnees sous la forme suivante:
    [noeud de depart, moment de depart, liste des points de passages possibles]
"""
def json_reader(json_data):
    data_list = []

    # Le noeud de depart n'aura necessairement aucune contrainte horaire,
    # ni de poids ou de volume
    start_node = [(json_data['start']['latitude'], json_data['start']['longitude']),
                   None, None, None, None
                   ]
    data_list.append(start_node)
    departure_hour = json_data['start']['departure_time']
    # conversion de la chaine de caractere de l'heure en une variable de format datetime
    departure_time = string_to_datetime(departure_hour)
    data_list.append(departure_time)
    car_size = json_data['start']['car_size']
    data_list.append(car_size)
    
    # points/noeuds de passage possible
    crossing_points = []
    points = json_data['items']
    for i in range(len(points)):
        # conversion des heures de contrainte pour chaque noeud,
        # puis ajout de chacun des noeuds a la liste des noeuds potentiellement traverses
        first_constraint_time = string_to_datetime(points[i]['available_since'])
        last_constraint_time = string_to_datetime(points[i]['available_until'])
        transit_point = [(points[i]['latitude'], points[i]['longitude'])]
        transit_point.append(first_constraint_time)
        transit_point.append(last_constraint_time)
        transit_point.append(points[i]['weight'])
        # Conversion du volume en valeur numerique
        transit_point.append(convert_volume(points[i]['volume']))
        # Verification de la validite des contraintes horaires
        transit_point = verif_datetime(transit_point)
        crossing_points.append(transit_point)
    data_list.append(crossing_points)
    return data_list


"""
ENTREE: node = tous les noeuds sous forme de liste
        departure = la date et heure de depart du premier noeud
OBJECTIF: calcule le parcours le plus avantageux
SORTIE: la liste des noeuds dans le meilleur ordre
"""
def json_writer(path):
    data = []
    points_list = []
    for i in range(len(path)):
        # sauvegarde des coordonnees dans l'ordre d'arrive
        points_list.append({"latitude": path[i][0][0], "longitude": path[i][0][1]})
    data = {"points": points_list}
    return data


'''
import json

array='{"start": {"latitude": 40.0,"longitude": 20.0, "departure_time": "9:00:00", "car_size": "moyen"},"items": [{"latitude": 30.0,"longitude": 15.0,"available_since": "9:00:00","available_until": "17:00:00"},{"latitude": 32.0,"longitude": 14.0,"available_since": "9:00:00","available_until": "17:00:00"},{"latitude": 32.0,"longitude": 13.0,"available_since": "10:00:00","available_until": "18:00:00"}]}'
array = '{"start": {"latitude": 40.0,"longitude": 20.0,"departure_time": "14:00:00","car_size": "moyen"},"items": [{"latitude": 30.0,"longitude": 15.0,"available_since": "9:00:00","available_until": "17:00:00","weight": 20,"volume": "peu encombrant"},{"latitude": 32.0,"longitude": 14.0,"available_since": "9:00:00","available_until": "17:00:00","weight": 100,"volume": "encombrant"},{"latitude": 32.0,"longitude": 13.0,"available_since": "10:00:00","available_until": "18:00:00","weight": 200,"volume": "tres encombrant"}]}'
json_data = json.loads(array)
data_list = json_reader(json_data)
for i in data_list:
    print(i)

start_constr_int = datetime.datetime(2017, 1, 16, 12, 0)
end_constr_int = datetime.datetime(2017, 1, 16, 14, 0)
path = ([(43.6005543, 1.4038282), None, None, None, None],
        [  (43.606521, 1.465111), None, None, 100, 'encombrant'],
        [  (43.620068, 1.435757), start_constr_int, end_constr_int, 20, 'peu encombrant'])
print(json_writer(path))
'''