# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: capacite.py version 1.0.0
"""

# Definition des capacites maximales des vehicules
MAX_WEIGHT_SMALL_VEHICLE = 500
MAX_WEIGHT_MEDIUM_VEHICLE = 800
MAX_WEIGHT_BIG_VEHICLE = 1000
MAX_VOLUME_SMALL_VEHICLE = 8
MAX_VOLUME_MEDIUM_VEHICLE = 12
MAX_VOLUME_BIG_VEHICLE = 16
# Valeurs numeriques des volumes rattaches aux textes descriptifs
SMALL_VOLUME = 1
MEDIUM_VOLUME = 3
BIG_VOLUME = 8


"""
ENTREE: un volume (sous forme de texte: "(peu/tres) encombrant")
OBJECTIF: convertir de facon arbitraire la valeurs qualitative en valeur quantitative
SORTIE: le volume quantifie
"""
def convert_volume(qual_volume):
    if qual_volume == "tres encombrant":
        quant_volume = BIG_VOLUME
    elif qual_volume == "encombrant":
        quant_volume = MEDIUM_VOLUME
    else: # qual_volume == "peu encombrant"
        quant_volume = SMALL_VOLUME
    return quant_volume


"""
ENTREE: poids_max = le poids que peut prendre la voiture
        volume_max = le volume que peut prendre la voiture
        current_weight = le poids qu'on a actuellement
        current_volume = le volume qu'on a actuellement
        arrival_node = le noeud de destination
OBJECTIF: test de la capacite car elle sera utilisee plusieurs fois dans la fonction estimate_capacity
SORTIE: le nouveau poids et volume, "inf" si on depasse la capacite
"""
def capacity_test(max_weight, max_volume, current_weight, current_volume, arrival_node):
    # On ajoute au poids et au volume actuel ceux de l'annonce.
    sum_weight = current_weight + arrival_node[3]
    sum_volume = current_volume + arrival_node[4]
    # On verifie que aucune des 2 valeurs maximales n'est depassee.
    if sum_weight <= max_weight and sum_volume <= max_volume:
            return sum_weight, sum_volume
    elif sum_weight <= max_weight and sum_volume > max_volume:
            return sum_weight, float("inf")
    elif sum_weight > max_weight and sum_volume <= max_volume:
            return float("inf"), sum_volume
    else: # sum_weight > max_weight and sum_volume > max_volume
            return float("inf"), float("inf")

"""
ENTREE: car_size = la taille de la voiture (petit, moyen, grand)
        current_weight = le poids qu'on a actuellement
        current_volume = le volume qu'on a actuellement
        arrival_node = le noeud de destination
OBJECTIF: calcule poids et volume en fonction de la voiture
SORTIE: le nouveau poids et volume, "inf" si on depasse la capacite, en fonction de la voiture
"""
def estimate_capacity(car_size, current_weight, current_volume, arrival_node):
    if car_size == "petit" :
        volume_max = MAX_VOLUME_SMALL_VEHICLE
        poids_max = MAX_WEIGHT_SMALL_VEHICLE
        return capacity_test(poids_max, volume_max, current_weight, current_volume, arrival_node)
    elif car_size == "moyen" :
        volume_max = MAX_VOLUME_MEDIUM_VEHICLE
        poids_max = MAX_WEIGHT_MEDIUM_VEHICLE
        return capacity_test(poids_max, volume_max, current_weight, current_volume, arrival_node)
    else: #carSize == "grand"
        volume_max = MAX_VOLUME_BIG_VEHICLE
        poids_max = MAX_WEIGHT_BIG_VEHICLE
        return capacity_test(poids_max, volume_max, current_weight, current_volume, arrival_node)

'''
# test des fonctions
arrival_node = [(43.6005543,1.4038282),  None, None, 100, 1]
print(capacity_test(800, 12, 600, 6, arrival_node))
arrival_node = [(43.6005543,1.4038282),  None, None, 200, 8]
print(estimate_capacity("moyen", 600, 6, arrival_node))
arrival_node = [(43.6005543,1.4038282),  None, None, 300, 8]
print(capacity_test(800, 12, 600, 6, arrival_node))
print(estimate_capacity("moyen", 600, 6, arrival_node))
print(estimate_capacity("grand", 600, 6, arrival_node))
'''