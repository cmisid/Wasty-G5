# Wasty-G5


En parametres d'entree, nous aurons le plus souvent (dans quasiment toutes nos fonctions) une liste de noeuds (ou points), ainsi qu'une heure de depart theorique choisie par l'utilisateur (pratique pour les contraintes horaires).

Un noeud (dans nos fonctions) est une liste qui comprend:

- des coordonnees GPS (latitude, longitude), on aura besoin des coordonnees GPS du point de depart (attribut user\_location de l'entite Users) comme des coordonnees GPS de chacun des points de passage potentiels (attribut advert\_adress (pour avoir location de Addresses) de Adverts)

- l'heure de debut de l'intervalle de la contrainte horaire (attribut constraint\_time\_begin de l'entite Adverts)

- l'heure de fin de l'intervalle de la contrainte horaire (attribut constraint\_time\_end de l'entite Adverts)


Il est possible qu'il n'y ait pas de contraintes horaires (valeurs None possibles).

(Pas encore fait pour le noeud mais devra etre fait):

- un volume (attribut volume de l'entite Adverts) (choix parmi 'peu encombrant'/'encombrant'/'tres encombrant')

- un poids (attribut weight de l'entite Adverts) (nombre entier)

On peut  aussi avoir besoin pour ce qui est evoque ci-dessus d'entrees supplementaires:

- de la taille de la voiture de l'utilisateur (attribut car_size de Users, choix parmi 'petit'/'moyen'/'grand').

On devrait pouvoir gerer des valeurs non renseignees pour la taille de la voiture.

Actuellement, avec les fonctions du fichier "calc_itin_best_score.py", on renvoie un itineraire juge comme le plus malin.

Le but est d'obtenir un score pour chaque parcours pour retenir celui qui aurait le meilleur, le score evolue pour chaque trajet entre 2 points.

Le score de temps est calcule selon:

- le temps de trajet theorique entre 2 points

- le moment d'arrivee au noeud d'arret (avant/pendant/apres l'intervalle de contrainte horaire)

Pour gerer la capacite max, on relevera le poids et le volume de ce que l'on recupere pour verifier qu'on ne depassera pas les capacites de la voiture.



Le point de départ noté (le champ `start`) doit contenir les champs suivants:

- `latitude`, un nombre flottant
- `longitude`, un nombre flottant
- `departure_time`, une chaîne de charactères "HH:MM:SS"

En plus:

- `car_size`, une chaîne de caractères "petit/moyen/grand"

Chaque point de la liste des points (le champ `points`) doit contenir les champs suivants:

- `latitude`, un nombre flottant
- `longitude`, un nombre flottant
- `available_since`, une chaîne de charactères "HH:MM:SS"
- `available_until`, une chaîne de charactères "HH:MM:SS"

En plus:

- `volume`, une chaîne de charactères "peu encombrant/encombrant/très encombrant"
- `weight`, un nombre entier

Le réponse renvoyé est une liste de points (dont le premier est le point de départ) contenant les champs suivants:

- `latitude`, un nombre flottant
- `longitude`, un nombre flottant