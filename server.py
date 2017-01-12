# -*- coding: utf-8 -*-
"""
@author: Groupe[5]
fichier: server.py version 2.0.0
(ajout: gestion de la capacite maximale)
"""

from flask import Flask, jsonify, request

from manage_json import json_reader, json_writer
from calc_itin_best_score import shortest_path

app = Flask(__name__)

@app.route('/')
def index():
    payload = {
        'test_1': 0.8,
        'test_2': 'meuble'
    }
    return jsonify(payload)

"""
ENTREE: on recupere les donnees (point de depart et points de passage potentiels)
        en json via une requete
OBJECTIF: integration de notre calcul de meilleur parcours avec le groupe 2
SORTIE: la liste des noeuds dans un format json
"""
@app.route('/optimize-itinerary', methods=['POST'])
def optimize_itinerary():
    payload = request.get_json()
    # Adaptation des donnees json (dictionnaire) sous une forme adaptee
    # a nos fonctions.
    data_list = json_reader(payload)
    nodes = data_list[3]
    # On met le noeud de depart en tete de la liste des noeuds
    nodes.insert(0, data_list[0])
    departure_time = data_list[1]
    car_size = data_list[2]
    # Calcul du meilleur parcours
    itinerary = shortest_path(nodes, departure_time, car_size)
    # Adaptation de nos resultats sous un format json adequat
    points = json_writer(itinerary)
    return jsonify(points)


if __name__ == '__main__':
    app.run(debug=True)
