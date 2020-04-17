# RRFTracker
FAQ à l'attention des admins.


# Comment obtenir des informations sur la BF cumulée ?

En CLI, l'outil `stats.py` permet d'obtenir la BF cumulée au quotidien, salon par salon ainsi que le cumul sur **le mois en cours** :

`python /opt/RRFTracker/tools/analyse/stats.py`

Par défaut, vous obtiendrez les données du mois en cours. Mais il est aussi possible d'obtenir les informations antérieures. Par exemple, pour obtenir les informations du mois de **février 2020**, on utilisera la commande :

`python /opt/RRFTracker/tools/analyse/stats.py --month 2020-02`

Il est même possible d'obtenir les informations d'une semaine spécifique de l'année en cours en entrant son numéro. Par exemple, pour **la semaine 11 de l'année 2020** (première semaine de confinement, HI) :

`python /opt/RRFTracker/tools/analyse/stats.py --week 11`

> Cette fonctionnalité ne marche que pour l'année en cours.

# Comment obtenir des informations sur la BF cumulée depuis les différents links du RRF ?

En CLI, l'outil `top.py` permet d'obtenir la BF cumuluée, link par link depuis X jours. Par exemple, sur les 90 derniers jours, on utilisera la commande :

`/opt/RRFTracker/tools/analyse/top.py --days 90`

> La BF cumulée affichée est calculée tous salons confondus mais hors FON.

À noter que si vous voulez uniquement cibler un link, la commande `grep` est votre ami. Par exemple, pour le link de Jean-François F1EVM sur les 30 derniers jours, on utilisera la commande :

`/opt/RRFTracker/tools/analyse/top.py --days 30 | grep 'F1EVM'`






