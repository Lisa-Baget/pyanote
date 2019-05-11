#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.accords

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de construire des accords.
"""

ACCORDS = {
    "aucun": [0],
    "majeur": [0, 4, 7],
    "mineur": [0, 3, 7],
    "augmenté": [0, 4, 8],
    "diminué": [0, 3, 6],
    "sixième majeure": [0, 4, 7, 9],
    "sixième mineure": [0, 3, 7, 9],
    "septième": [0, 4, 7, 10],
    "septième majeure": [0, 4, 7, 11],
    "septième mineure": [0, 3, 7, 10],
    "septième augmentée": [0, 4, 8, 10],
    "septième diminuée": [0, 3, 6, 9]
}

def construire_accord(note, nom_accord):
    accord = []
    for mod in ACCORDS[nom_accord]:
        accord.append(note + mod)
    return accord

if __name__ == "__main__":
    import pyanote.notes as notes
    print("================================")
    print("Test de construction d'accords")
    print("================================")
    LISTE = [["C", "mineur"], ["A#5", "majeur"], ["G3", "septième diminuée"]]
    for note_chaine, nom_accord in LISTE:
        note_nombre = notes.note_vers_nombre(note_chaine)
        accord = construire_accord(note_nombre, nom_accord)
        print("L'accord", nom_accord, "sur la note", note_chaine, "est", accord)

