# Wasty-G5


En parametres d'entree, nous aurons le plus souvent (dans quasiment toutes nos fonctions)
une liste de noeuds (ou points),
ainsi qu'une heure de depart theorique choisie par l'utilisateur
(pratique pour les contraintes horaires)

Un noeud lui-meme est une liste qui comprend:
	des coordonnees GPS (latitude, longitude) (voir *)
		(couple de 2 float)
	l'heure de debut de l'intervalle de la contrainte horaire (date complete)
		(attribut constraint_time_begin de l'entite Adverts)
	l'heure de fin de l'intervalle de la contrainte horaire (date complete)
		(attribut constraint_time_end de l'entite Adverts)
	un item prix (attribut price de l'entite Adverts)
		(nombre entier en euros)

(*) on aura besoin des coordonnees GPS du point de depart (attribut user_location de l'entite Users)
comme des coordonnees GPS de chacun des points de passage potentiels
(attribut advert_adress (pour avoirlocation de Addresses) de Adverts)


Il est possible qu'il n'y ait pas de contraintes horaires (valeurs None possibles)
Une absence de prix serait penalisant dans sa gestion.


(pas encore fait pour le noeud mais devra etre fait):
	un volume (attribut volume de l'entite Adverts)
		(choix parmi 'peu encombrant'/'encombrant'/'tres encombrant')
	un poids (attribut weight de l'entite Adverts)
		(nombre entier en kg)
On peut  aussi avoir besoin avec ce qui est ci-dessus (le tout va ensemble),
de la taille de la voiture de l'utilisateur (attribut car_size de Users,
choix parmi 'petit'/'moyen'/'grand').
On devrait pouvoir gerer des valeurs non renseignees pour la taille de la voiture.




Actuellement, avec les fonctions du fichier "calc_itin_best_score.py",
on renvoie un itineraire juge comme le plus malin.

Le but est d'obtenir un score pour chaque parcours pour retenir
celui qui aurait le meilleur, le score evolue pour chaque trajet entre 2 points.

Le score est calcule selon:
	le temps de trajet theorique entre 2 points
	le moment d'arrivee au noeud d'arret (avant/pendant/apres l'intervalle de contrainte horaire)
	le prix qu'on trouve a ce noeud d'arret

A rajouter:
	le poids et le volume de ce que l'on recupere pour verifier qu'on ne
		depassera pas les capacites de la voiture.

Le parcours juge le plus malin ne passera pas necesserairement
par tous les points de passages possibles.