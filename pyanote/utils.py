#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.utils

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de lire des informations simples dans un fichier binaire Midi.
"""

def verifier(fichier, mot_clé, msg_erreur):
    ''' Verifie si mot_clé est dans le fichier, sinon envoie une erreur avec msg_erreur.

    Dans tous les cas avance de len(mot_clé) dans le fichier.  
    '''
    if fichier.read(len(mot_clé)) != mot_clé:
        raise TypeError(msg_erreur)

def lire_entier(fichier, nb_octets):
    ''' Lit un entier codé sur nb_octets dans le fichier.
    '''
    entier = 0
    for i in range(nb_octets): #commence par poid fort
        entier = entier + ord(fichier.read(1)) * 256**(nb_octets-i-1) # ord transforme 1 octet binaire en entier (
    return entier

def lire_entier_variable(fichier):
    ''' Lit un entier codé sur un nombre variable d'octets dans le fichier (d'après le format MIDI).

    Continue à lire des octets dans que le premier bit est à 1.
    '''
    entier = 0
    octet = ord(fichier.read(1))
    while octet >= 128:
        entier = entier * 128 + octet - 128
        octet = ord(fichier.read(1))
    return entier * 128 + octet

def avancer(fichier, nb_octets):
    '''Avance de nb_octets dans le fichier sans les lire.
    '''
    fichier.seek(nb_octets, 1) #1 a partir de la position ou l'on est / 0 debut fichier

def lire_chaine(fichier, taille, liste_codages=['utf-8']): # UTF-8 par défaut
    ''' Lit une chaine binaire de taille octets et essaie de la transformer en une chaine en
    utilisant un des codages de liste_codages.

    Les codages sont essayés dans l'ordre de la liste et la fonction renvoie une chaine binaire
    si aucun des codages n'a pu etre utilisé.
    '''
    chaine = fichier.read(taille)
    for codage in liste_codages: # pour chaque codage dans la liste en parametre
        try: # essayer de décoder
            return chaine.decode(codage)
        except UnicodeDecodeError: # siça marche pas
            pass # rien faire pour essayer un autre codage
    return chaine # si aucun codage a marché la chaine sera binaire

def lire_liste_octets(fichier, taille):
    ''' Lit taille entiers codés sur un octet et les stocke dans une liste.
    '''
    liste = []
    for i in range(taille): 
        liste.append(ord(fichier.read(1)))
    return liste

if __name__ == "__main__":
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    print("=========================================================")
    print("Test du fichier", nom_fichier)
    print("=========================================================")
    fichier = open(nom_fichier, 'rb')
    print("Verification du MThd: ", end="")
    try:
        verifier(fichier, b'MThd', "")
        print("OK")
    except TypeError:
        print("Erreur")
    taille_header = lire_entier(fichier, 4)
    print("Taille du header: ", taille_header, "octets")
    avancer(fichier, taille_header)
    print("Verification du premier MTrk: ", end="")
    try:
        verifier(fichier, b'MTrk', "")
        print("OK")
    except TypeError:
        print("Erreur")
    taille_piste = lire_entier(fichier, 4)
    print("Taille de la première piste: ", taille_piste, "octets")
    delta_time = lire_entier_variable(fichier)
    print("Valeur du premier delta time:", delta_time, "ticks")


