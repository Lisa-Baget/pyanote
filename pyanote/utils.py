#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.utils

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de lire des informations simples dans un fichier Midi.
"""

def verifier(fichier, mot_clé, msg_erreur):
    if fichier.read(len(mot_clé)) != mot_clé:
        raise TypeError(msg_erreur)

def lire_entier(fichier, nb_octets):
    entier = 0
    for i in range(nb_octets): #commence par poid fort
        entier = entier + ord(fichier.read(1)) * 256**(nb_octets-i-1) #ord transforme 1 octet binaire en entier (
    return entier

def lire_entier_variable(fichier):
    entier = 0
    octet = ord(fichier.read(1))
    while octet >= 128:
        entier = entier * 128 + octet - 128
        octet = ord(fichier.read(1))
    return entier * 128 + octet

def avancer(fichier, nb_octets):
    fichier.seek(nb_octets, 1) #1 a partir de la position ou l'on est / 0 debut fichier

def lire_chaine(fichier, taille):
    chaine = fichier.read(taille)
    for codage in ['utf-8', 'latin-1']: # rajouter si je trouve des fichiers ou ça suffit pas
        try:
            return chaine.decode(codage)
        except UnicodeDecodeError:
            pass
    return chaine