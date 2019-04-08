# RRFTracker_Web
Suivi temps réel de l'activité du réseau [RRF](https://f5nlg.wordpress.com/2015/12/28/nouveau-reseau-french-repeater-network/) (Réseau des Répéteurs Francophones) pour le Web. Ce projet est une déclinaison Web de la version développée pour [Spotnik](https://github.com/armel/RRFTracker_Spotnik).

## Présentation

Voici une liste des informations visibles:

### Résumé de la journée

Le résumé de la journée affiche plusieurs informations:

* Salon: RRF ou TEC,
* Date et heure courante,
* Nombre de passage en émission (de plus de 3 secondes...),
* Durée émission (cumul dans la journée),
* Nombre de noeuds actifs (étant passés en émission au moins 1 fois),
* Nombre de noeuds total.

### Activité heure par heure

Représentée sous forme d'histogramme, on peut y suivre l'activité du salon dans la journée. Le nombre de passage en émission y est représenté, heure par heure.

### Top 20 des noeuds les plus actifs

Egalement représenté sous forme d'histogramme, on peut y découvrir le classement des 20 noeuds les plus actifs de la journée. 

### Noeud en cours d'émission

En plus de l'indicatif du noeud en cours d'émission, une horloge affiche le temps de passage en émission.

### Derniers passages en émission

Ce tableau présente la liste des 10 derniers passages en émission, avec:

* L'horodatage,
* L'indicatif du noeud,
* La durée de passage en émission.

### Classement des noeuds actifs

Ce tableau présente le classement général de l'ensemble des noeuds étant passés en émission au moins 1 fois. On y observe:

* La position dans le classement,
* L'indicatif du noeud,
* Le nombre de passage en émission.

### Déclenchements « intempestifs »

Ce tableau présente le classement général des noeuds ayant fait l'objet de déclenchements « intempestifs » (volontaires ou non...). En particulier, un déclenchement est concidéré comme intempestifs quand de la BF a été détectée pendant moins de 3 secondes. On y observe:

* La position dans le classement,
* L'indicatif du noeud,
* Le nombre de déclenchements « intempestifs » en émission.
