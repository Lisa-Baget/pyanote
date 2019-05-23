#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.notes

(C) Lisa Baget, Matthieu Durand, 2018-2019

Ce module contient les transformations entre les noms de notes (par ex "C#4") et leur valeur MIDI.
"""

## Nom des notes pour les différentes langues
EN = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}
FR = {0: "Do", 2: "Ré", 4: "Mi", 5: "Fa", 7: "Sol", 9: "La", 11: "Si"}
DE = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "H"}
SP = {0: "Do", 2: "Re", 4: "Mi", 5: "Fa", 7: "Sol", 9: "La", 11: "Si"}
IT = SP

def nombre_vers_note(nombre, prefere='#', lang=EN):
    octave = (nombre // 12) - 1
    try:
        note = lang[nombre % 12]
    except KeyError: # si il y a une erreur, c'est que c'est un diese du precedent ou un bemol du suivant
        if prefere == '#': # on prefere prendre le diese
            note = lang[(nombre % 12) - 1] + '#'
        else: # on prefere prendre le bemol
            note = lang[(nombre % 12) + 1] + 'b'
    return note + str(octave)

def note_vers_nombre(chaine, lang=EN):
    dernier = -1 ## on va déchiffrer la chaîne à partir de la fin
    modificateur = 0
    try:
        octave = int(chaine[dernier]) ## si on a reussi a transformé le dernier caractère en entier, c'est l'octave
        dernier = dernier -1 # il faudra regarder l'avant-dernier
    except ValueError: # si ce n'était pas un entier
        octave = 4 # c'est l'octave par défaut
    if chaine[dernier] == '#':
        modificateur = 1
        dernier = dernier -1
    elif chaine[dernier] == 'b':
        modificateur = -1
        dernier = dernier -1
    if dernier != -1: ## si on a recupere un octave ou un modificateur
        chaine = chaine[:dernier + 1] ## on les enleve maintenant de la chaine
    valeur_note = None
    for cle in lang: # recherche de la clé associée à la valeur, pas super efficace
        # il faudrait peut-être construire une fois pour toute le dico inverse
        # pas un problçème pour l'instant
        if lang[cle] == chaine:
            valeur_note = cle
    if valeur_note is None:
        raise ValueError("Ceci n'est pas le nom d'une note dans ce langage.")
    return ((octave + 1) * 12) + valeur_note + modificateur


if __name__ == "__main__":
    print("==========================================")
    print("Test de nombre vers note")
    print("==========================================")
    LISTE_NOMBRES = [60, 82, 55]
    print("------------------------------------------")
    print("Version anglaise")
    print("------------------------------------------")
    for nombre in LISTE_NOMBRES:
        print("La note représentée par le nombre", nombre, "est", nombre_vers_note(nombre))
    print("------------------------------------------")
    print("Version française")
    print("------------------------------------------")
    for nombre in LISTE_NOMBRES:
        print("La note représentée par le nombre", nombre, "est", nombre_vers_note(nombre, '#', FR))
    print("------------------------------------------")
    print("Preference bemols")
    print("------------------------------------------")
    for nombre in LISTE_NOMBRES:
        print("La note représentée par le nombre", nombre, "est", nombre_vers_note(nombre, 'b'))
    print("==========================================")
    print("Test de note vers nombre")
    print("==========================================")
    LISTE_NOTES = ["C4", "Bb5", "A#5", "G3"]
    for note in LISTE_NOTES:
        print("Le nombre représenté par la note", note, "est", note_vers_nombre(note))
    print("==========================================")
    print("Le gros test pour tout verifier")
    print("==========================================")
    resultat = True
    for nombre in range(12, 127): ## test de la transformation inverse
        if note_vers_nombre(nombre_vers_note(nombre)) != nombre:
            resultat = False
    if resultat:
        print("Les nombres de 12 a 127 ont été vérifiés avec succés")
    else:
        ## C'est ce qui se passe avec des notes < 12 (octave = -1)
        ## il faudra le corriger si ça pose des problemes...
        print("OUPS")

    

    
    