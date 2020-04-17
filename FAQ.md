# RRFTracker
FAQ à l'attention des admins.


# Comment obtenir des informations sur la BF cumulée

En CLI, l'outil `stats.py` permet d'obtenir la BF cumulée au quotidien, salon par salon ainsi que le cumul sur le mois :

`python /opt/RRFTracker/tools/analyse/stats.py`

Par défaut, vous obtiendrez les données du mois en cours. Mais il est aussi possible d'obtenir les informations antérieures. Par exemple, pour obtenir les informations du mois de février 2020, on utilisera la commande :

`python /opt/RRFTracker/tools/analyse/stats.py --month 2020-02`

Il est même possible d'obtenir les informations d'une semaine spécifique en entrant son numéro :


