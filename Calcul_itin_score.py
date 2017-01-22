import math
import itertools
import googlemaps
import datetime
import json

RETRIEVAL_TIME = 5

'''
ENTREE: time = le temps de depart
        arrival_node = le noeud destination sous la forme [coordonnee, debut horraire, fin horraire, gain]
        duration = la duree du trajet entre le depart et la destination
OBJECTIF: donner le temps du trajet avec le possible temps d'attente
SORTIE: la duree totale en minute
'''
def time_between_node(time, arrival_node, duration):
    if arrival_node[1] != None and (time + datetime.timedelta(minutes = duration) + datetime.timedelta(minutes = RETRIEVAL_TIME)) < arrival_node[1]:
        result = arrival_node[1] - time
        return (result.total_seconds()/60 + RETRIEVAL_TIME)
    else:
        if arrival_node[2] != None and (time + datetime.timedelta(minutes = duration) + RETRIEVAL_TIME) > arrival_node[2]:
            return 100000
        else:
            return (duration/60 + RETRIEVAL_TIME)

'''
ENTREE: node = tous les noeuds sous forme de liste
        mode_transport = le mode de transport
        gmaps = pour utiliser google api avec la bonne cle
OBJECTIF: calcule tous les arcs entre les noeuds
SORTIE: retoure une liste d'arc sous la forme [1er noeud, 2eme noeud, distance en metre, duree en secondes]
'''
def calculate_path(node, mode_transport, gmaps):
  path = []
  for i in node:
      for j in node:
          if (j!=i) :
              distance = gmaps.distance_matrix(i[0],j[0],mode = mode_transport)
              path.append([i,j,distance["rows"][0]["elements"][0]["distance"]["value"],distance["rows"][0]["elements"][0]["duration"]["value"]])
  return path

'''
ENTREE: node = tous les noeuds sous forme de liste
        alpha = critere d'importance de la duree
        beta = critere d'importance du gain
        departure = la date et temps de depart
OBJECTIF: calcule le parcours le plus avantageux
SORTIE: la liste des noeuds dans le meilleur ordre
'''
def shortest_path(node, aplha, beta, departure):
    score = 0
    time = 0
    date = departure
    cp=0
    result = []
    gmaps = googlemaps.Client(key='AIzaSyDRpQO4ww7fK610iK5Np-GeiPbCSTuaqec')
    itinerary = calculate_path(node, "driving", gmaps)
    
    for nb_node in range(2,len(node) + 1):
        for subset in itertools.permutations(node, nb_node):
            if(subset[0] == node[0]):
                i = 0
                while (time < 100000) and i < (len(subset) - 1):
                    j = 0
                    while (time < 100000) and j <(len(itinerary)):
                        if itinerary[j][0] == subset[i] and itinerary[j][1] == subset[i + 1]:
                            time = time_between_node(date, subset[i + 1] , itinerary[j][3])
                            date = date + datetime.timedelta(minutes = time)
                            score = score + (alpha*time - beta*subset[i + 1][3])
                        j = j + 1
                    i = i + 1
                full_score = score
                if(cp == 0):
                    min_score = full_score
                    cp = cp + 1
                    result = subset
                else:
                    if(min_score > full_score):
                        min_score = full_score
                        result = subset
                score = 0
    return result

#test pour les horaires
dep = datetime.datetime(2017,1,6,11,0,0)
a = datetime.datetime(2017,1,6,12,0,0)
b = datetime.datetime(2017,1,6,14,0,0)

#test noeud
test_noeud = [[(43.6005543,1.4038282),None,None,0,5],[(43.620068, 1.435757),None,None,10,5],[(43.606521, 1.465111),None,None,10,5],[(43.602729, 1.452065),None,None,0,5],[(43.612238, 1.427174),None,None,0,5]]
alpha = 0.3 #importance de la duree du trajet
beta = 1 #importance du gain


print shortest_path(test_noeud, alpha, beta, dep)
