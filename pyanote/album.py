#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.album

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de récupérer sous forme d'album toutes les informations contenues
dans un fichier Midi. L'album est un dictionnaire qui contient toutes les informations d'un resume, plus une 
liste de chansons, c'est a dire une liste de listes d'evenements.

Format 0: L'album ne contient qu'une chanson, qui est exactement la piste 0 

Format 1: L'album ne contient qu'une chanson, qui est obtenue en fusionnant toutes les pistes.

Format 2: L'album contient plusieurs chansons, une pour chaque piste.
"""
import pyanote.piste as piste
import pyanote.resume as resume
import heapq

def creer_album(nom_fichier):
    ''' Cree un album, qui est un résumé augmenté par une liste de chansons.
    '''
    album = resume.creer_resume(nom_fichier) # dans l'album il y a toutes les infos du résumé
    album["chansons"] = []
    for num_piste in range(album['nb_pistes']):
        album["chansons"].append(piste.creer_piste(album, num_piste))
    if album['format'] == 1:
        album["chansons"] = [fusionner_pistes(album["chansons"])]
    return album

def fusionner_pistes(liste_pistes):
    ''' Fusionne les pistes d'une liste (chaque piste est une liste d'evenements) en une seule piste équivalente.
    '''
    for piste in liste_pistes:
        transformer_temps_absolu(piste)
    ##si j'ai L = [a, b, c], la fonction f(L) appelle f avec un seul argument qui est la liste L
    ## mais la fonction f(*L) appelle f avec tous les elements de la liste, et est donc equivalente
    ## à f(a, b, c)
    fusion = list(heapq.merge(*liste_pistes)) # https://www.geeksforgeeks.org/merge-two-sorted-arrays-python-using-heapq/
    transformer_temps_relatif(fusion)
    return fusion
    
def transformer_temps_absolu(piste):
    ''' Transforme les delta_temps d'une piste en temps absolu.
    
    Par exemple [[0, 0, 'A'], [10, 0, 'B'], [0, 0, 'C'], [20, 0, 'D']] deviendra
    [[0, 0, 'A'], [10, 0, 'B'], [10, 0, 'C'], [30, 0, 'D']]. Ne crée pas une autre piste
    mais la modifie.
    '''
    temps = 0
    for evenement in piste:
        evenement[0] = evenement[0] + temps
        temps = evenement[0]

def transformer_temps_relatif(piste):
    ''' Transforme une piste où les temps sont donnés en temps absolus pour que ces temps
    deviennent des delta_temps (temps relatifs).

    Par exemple [[0, 0, 'A'], [10, 0, 'B'], [10, 0, 'C'], [30, 0, 'D']] deviendra
    [[0, 0, 'A'], [10, 0, 'B'], [0, 0, 'C'], [20, 0, 'D']]. Ne crée pas une autre piste
    mais la modifie.
    '''
    temps = 0
    for evenement in piste:
        nouveau_temps = evenement[0]
        evenement[0] = evenement[0] - temps
        temps = nouveau_temps

if __name__ == "__main__":
    print("=============================================================================")
    print("Exemple de fusion avec des pistes simplifiées (les messages sont des lettres)")
    print("=============================================================================")
    liste1 = [[0, 1, 'B'], [10, 1, 'A'], [20, 1, 'S']]
    liste2 = [[10, 2, 'V'], [10, 2, 'L'], [10, 2, 'A']]
    liste3 = [[0, 3, 'R'], [10, 3, 'O'], [0, 3, ' '], [10, 3, 'I']]
    print("Liste 1 = ", liste1)
    print("Liste 2 = ", liste2)
    print("Liste 3 = ", liste3)
    print("=============================================================================")
    print("Résultat de la fusion:")
    print("=============================================================================")
    fusion = fusionner_pistes([liste1, liste2, liste3])
    print(fusion)

    # suivant l'environnement, peut avoir besoin de mettre un chemin different
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    print("===========================")
    print("Exemple de création d'album")
    print("===========================")
    album = creer_album(nom_fichier)
    print("Le fichier contient", album['nb_pistes'], "pistes.")
    print("L'album contient", len(album["chansons"]), "chanson(s).")
    print('---------------------------')
    for i in range(len(album["chansons"])):
        print("La taille de la chanson", i, "est", len(album["chansons"][i]), "evenements.")
    ## Ce test montre que certaines pistes se sont arretees avant la fin
    ## Probleme ou pas? J'ai pas vu dans le format midi qu'elles devaient finir en meme temps
    print('Les 12 derniers evenements de la premiere chanson sont:')
    print(album["chansons"][0][-12:])


        
