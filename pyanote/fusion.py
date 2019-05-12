#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.fusion

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net> et Phandaal <https://github.com/phandaal> (pour l'algorithme)

Ce module contient les fonctions permettant de fusionner plusieurs listes d'évènements (des pistes).

La liste unique d'évènements obtenus est équivalente à la juxtaposition de toutes les listes d'évènements passées en paramètre.
"""

def fusionner_pistes(liste_pistes):
    ''' Fusionne les pistes d'une liste (chaque piste est une liste d'evenements) en une seule piste équivalente.
    '''
    liste_fusion = [] # c'est la liste qui contiendra les evenements
    # Si liste_indexs[i] = j, ça veut dire que le prochain candidat de la piste i est le j-eme evenement
    # de cette piste, c'est à dire liste_pistes[i][j]
    liste_indexs = [0] * len(liste_pistes)
    ## Si liste_temps[i] = t, ça veut dire que le prochain evenement de la piste i doit se passer au temps absolu t.
    liste_temps = []
    for num_piste in range(len(liste_pistes)): # initialisation de la liste_temps avec les delta temps des premiers evenements de chaque piste
        evenement = lire_evenement(liste_pistes, num_piste, liste_indexs) # premier evenement de la piste numero num_piste
        liste_temps.append(evenement[0])
    temps_courant = 0
    num_piste = calculer_index_prochain(liste_temps)
    infini = float('inf') # infini https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
    while liste_temps[num_piste] < infini: # si le plus petit temps est infini c'est qu'on a tout fini
        delta_temps = liste_temps[num_piste] - temps_courant # calcul de l'intervalle de temps pour cet evenement
        temps_courant = liste_temps[num_piste] # le nouveau temps courant est le temps absolu de l'evenement
        evenement = lire_evenement(liste_pistes, num_piste, liste_indexs) #recupeper l'evenement
        liste_fusion.append([delta_temps, evenement[1], evenement[2]]) # le rajouter à la liste avec le nouveau delta-temps
        if liste_indexs[num_piste] + 1 == len(liste_pistes[num_piste]): # on a fini cette liste
            liste_temps[num_piste] = infini # comme ça il ne sera choisi que quand toutes les pistes sont finies
        else: # on doit continuer donc mise a jour de liste_indexs et liste_temps
            liste_indexs[num_piste] = liste_indexs[num_piste] + 1 # le suivant dans la piste
            prochain_evenement = lire_evenement(liste_pistes, num_piste, liste_indexs) # correspond au nouvel index
            liste_temps[num_piste] = temps_courant + prochain_evenement[0] # nouveau temps absolu
        num_piste = calculer_index_prochain(liste_temps) # calcul du prochain avant de recommencer la boucle
    return liste_fusion

def lire_evenement(liste_pistes, num_piste, liste_indexs):
    ''' Retourne le prochain evenement dans la piste num_piste (liste_pistes[num_piste]), en fonction des informations dans liste_indexs.
    '''
    return liste_pistes[num_piste][liste_indexs[num_piste]]

def calculer_index_prochain(liste_temps):
    ''' Retourner l'index du plus petit element dans liste_temps.

    C'est la même que dans une fonction de tri sauf qu'on retourne la position et pas l'element.
    '''
    index = 0
    for i in range(1, len(liste_temps)):
        if liste_temps[i] < liste_temps[index]:
            index = i
    return index

if __name__ == "__main__":
    print("=============================================================================")
    print("Exemple de fusion avec des pistes simplifiées (les messages sont des lettres)")
    print("=============================================================================")
    liste1 = [[0, 'B', 1], [10, 'A', 1], [20,  'S', 1]]
    liste2 = [[10, 'V', 2], [10, 'L', 2], [10, 'A', 2]]
    liste3 = [[0, 'R', 3], [10, 'O', 3], [0, ' ', 3], [10, 'I', 3]]
    print("Liste 1 = ", liste1)
    print("Liste 2 = ", liste2)
    print("Liste 3 = ", liste3)
    print("=============================================================================")
    print("Résultat de la fusion:")
    print("=============================================================================")
    print(fusionner_pistes([liste1, liste2, liste3]))
    