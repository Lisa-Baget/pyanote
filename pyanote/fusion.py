#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.fusion

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de fusionner plusieurs listes d'évènements (des pistes).

La liste unique d'évènements obtenus est équivalente à la juxtaposition de toutes les listes d'évènements passées en paramètre.
"""

def fusionner_pistes(liste_pistes):
    ''' Fusionne les pistes d'une liste (chaque piste est une liste d'evenements) en une seule piste équivalente.
    '''
    liste_fusion = [] # c'est la liste qui contiendra les evenements
    liste_indexs = [0] * len(liste_pistes)
    liste_temps = initialiser_liste_temps(liste_pistes)
    temps_courant = 0
    num_piste = calculer_index_prochain(liste_temps)
    infini = float('inf') # infini https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
    while liste_temps[num_piste] < infini: # si le plus petit temps est infini c'est qu'on a tout fini
        delta_temps = liste_temps[num_piste] - temps_courant
        temps_courant = liste_temps[num_piste]
        evenement = lire_evenement(liste_pistes, num_piste, liste_indexs[num_piste])
        liste_fusion.append([delta_temps, evenement[1], evenement[2]])
        if liste_indexs[num_piste] + 1 == len(liste_pistes[num_piste]): # on a fini cette liste
            liste_temps[num_piste] = infini
        else:
            index = liste_indexs[num_piste] + 1
            liste_indexs[num_piste] = index
            liste_temps[num_piste] = temps_courant + liste_pistes[num_piste][index][0]
        num_piste = calculer_index_prochain(liste_temps)
    return liste_fusion

def initialiser_liste_temps(liste_pistes):
    liste_temps = []
    for num_piste in range(len(liste_pistes)):
        evenement = lire_evenement(liste_pistes, num_piste, 0) # premier evenement de la piste numero num_piste
        temps = evenement[0]
        liste_temps.append(temps)
    return liste_temps

def lire_evenement(listes_evenements, num_piste, index):
    return listes_evenements[num_piste][index]

def calculer_index_prochain(liste_temps):
    index = 0
    for i in range(1, len(liste_temps)):
        if liste_temps[i] < liste_temps[index]:
            index = i
    return index

if __name__ == "__main__":
    print("Pistes simplifiées (les messages sont des lettres):")
    liste1 = [[0, 'B', 1], [10, 'A', 1], [20,  'S', 1]]
    liste2 = [[10, 'V', 2], [10, 'L', 2], [10, 'A', 2]]
    liste3 = [[0, 'R', 3], [10, 'O', 3], [0, ' ', 3], [10, 'I', 3]]
    print("Liste 1 = ", liste1)
    print("Liste 2 = ", liste2)
    print("Liste 3 = ", liste3)
    print("==================== Fusion des 3 listes")
    print(fusionner_pistes([liste1, liste2, liste3]))
    