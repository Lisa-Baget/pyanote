#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.resume

(C) Lisa Baget, 2018-2019

Ce module contient les fonctions permettant de construire un dictionnaire qui contient les informations
essentielles d'un fichier Midi, apres une lecture partielle.

TODO: Comprendre le deuxieme format de tempo, mais il faut trouver un fichier exemple
"""
import pyanote.utils as utils

def creer_resume(nom_fichier):
    ''' Retourne un dictionnaire contenant les informations nécessaires à l'utilisation d'un fichier MIDI.
        
       Voir exemple en fin de fichier pour la structure du dictionnaire.
    '''
    fichier = open(nom_fichier, "rb") # r = read b = binaire
    resume = {"fichier": nom_fichier, "resumes_pistes": []} # dictionnaire
    lire_header(fichier, resume) # remplissage du dico avec infos du header
    for numero_piste in range(resume['nb_pistes']):
        resume["resumes_pistes"].append(creer_resume_piste(fichier, numero_piste))
    fichier.close()
    return resume

def lire_header(fichier, resume):
    ''' Complete le resume avec les informations contenues dans le header.
    '''
    utils.verifier(fichier, b'MThd', "Ce n'est pas un fichier Midi")
    taille_header = utils.lire_entier(fichier, 4) 
    resume["format"] = utils.lire_entier(fichier, 2)
    resume["nb_pistes"] = utils.lire_entier(fichier, 2)
    verifier_format(resume) # test d'erreurs
    resume["ticks/noire"] = utils.lire_entier(fichier, 2)
    verifier_tempo(resume)
    utils.avancer(fichier, taille_header - 6) # ces octets sont reserves aux constructeurs MIDI        

def verifier_format(resume):
    ''' Verifie si le format existe et si il est compatible avec le combre de pistes.

    Renvoie une erreur sinon.
    '''
    if resume["format"] > 2:
        raise ValueError("Format MIDI inconnu.")
    if resume["format"] == 0 and resume["nb_pistes"] != 1:
        raise ValueError("Le nombre de pistes ne correspond pas au format MIDI 0")

def verifier_tempo(resume):
    ''' Renvoie une erreur si le tempo est au format SMPTE.
    '''
    if resume["ticks/noire"] >= 128*256: # le premier bit du premier octet est à 1
        raise ValueError("Pyanote ne prend pas en compte le tempo au format SMPTE.")

def creer_resume_piste(fichier, num_piste):
    ''' Retourne un dictionnaire contenant les informations nécessaires à la lecture
    de la piste num_piste.
    '''
    utils.verifier(fichier, b'MTrk', "Ce n'est pas le début d'une piste")
    taille_piste = utils.lire_entier(fichier, 4)
    position = fichier.tell() #retourne le nombre d'octets passé depuis le début
    utils.avancer(fichier, taille_piste - 3) # -3 pour verifier le meta "fin de piste"
    utils.verifier(fichier, b'\xFF\x2F\x00', "Ce n'est pas la fin d'une piste")
    return {'id' : num_piste, 'début' : position, 'fin' : position + taille_piste}

if __name__ == "__main__":
    # suivant l'environnement, peut avoir besoin de mettre un chemin different
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    print("=================================")
    print("Exemple de résumé de fichier MIDI")
    print("=================================")
    print(creer_resume(nom_fichier))

