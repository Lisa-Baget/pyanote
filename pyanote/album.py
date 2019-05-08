#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.album

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de récupérer sous forme d'album tous les evenements contenus
dans un fichier Midi. L'album est toujours une liste de titres, c'est a dire une liste de liste d'evenements.

Format 0: L'album ne contient qu'un titre, qui est exactement la piste 0 

Format 1: L'album ne contient qu'un titre, qui est obtenu en fusionnant toutes les pistes.

Format 2: L'album contient plusieurs titres, un pour chaque piste.
"""
import pyanote.piste as piste
import pyanote.fusion as fusion

def creer_album(resume):
    pistes = []
    for num_piste in range(resume['nb_pistes']):
        pistes.append(piste.creer_piste(resume, num_piste))
    if resume['format'] == 1:
        return [fusion.fusionner_pistes(pistes)]
    else:
        return pistes

if __name__ == "__main__":
    import pyanote.resume as res
    # suivant l'environnement, peut avoir besoin de mettre un chemin different
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    resume = res.creer_resume(nom_fichier)
    album = creer_album(resume)
    print("L'album contient", len(album), "titre(s).")
    for i in range(len(album)):
        print("La taille du titre", i, "est", len(album[i]), "evenements")
    

        
