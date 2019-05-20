#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.accords

(C) Lisa Baget et Matthieu Durand, 2018-2019

Ce module contient les fonctions permettant de construire un accord (c'est à dire une liste)
de notes à partir d'une note de base (la fondamentale) et du nom de l'accord.

TO DO: rajouter des accords, inversion des accords, reconnaitre un accord à partir d'une liste
de notes (compliqué).
"""

ACCORDS = {
    "aucun": [0], "majeur": [0, 4, 7], "mineur": [0, 3, 7], "augmente": [0, 4, 8], "diminue": [0, 3, 6],
    "sixieme majeure": [0, 4, 7, 9], "sixieme mineure": [0, 3, 7, 9], "septieme": [0, 4, 7, 10], 
    "septieme majeure": [0, 4, 7, 11], "septieme mineure": [0, 3, 7, 10],
    "septieme augmentee": [0, 4, 8, 10], "septieme diminuee": [0, 3, 6, 9]
}

def construire_accord(note_fondamentale, nom_accord):
    ''' Cette fonction construit un accord (une liste de notes)
    à partir d'une note fondamentale et d'un nom d'accord. Les noms d'accords
    possibles sont les clés du dictionnaire pyanote.accords.ACCORDS
    '''
    accord = []
    for intervalle in ACCORDS[nom_accord]:
        accord.append(note_fondamentale + intervalle)
    return accord

if __name__ == "__main__":
    import pyanote.notes as notes
    print("================================")
    print("Test de construction d'accords")
    print("================================")
    LISTE = [["C", "mineur"], ["A#5", "majeur"], ["G3", "septieme diminuee"]]
    for note_chaine, nom_accord in LISTE:
        note_nombre = notes.note_vers_nombre(note_chaine)
        accord = construire_accord(note_nombre, nom_accord)
        print("L'accord", nom_accord, "sur la note", note_chaine, "est", accord)


