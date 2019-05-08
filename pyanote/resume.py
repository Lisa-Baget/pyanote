#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.resume

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de construire un dictionnaire qui contient les informations
essentielles d'un fichier Midi, apres une lecture partielle.
"""
import pyanote.utils as utils

def creer_resume(nom_fichier):
    ''' Retourne un dictionnaire contenant les informations nécessaires à l'utilisation d'un fichier MIDI.
        
       Voir exemple en fin de fichier pour la structure du dictionnaire.
    '''
    fichier = open(nom_fichier, "rb") # r = read b = binaire
    resume = {"fichier": nom_fichier, "pistes": []} # dictionnaire
    lire_header(fichier, resume) # remplissage du dico avec infos du header
    for numero_piste in range(resume['nb_pistes']):
        resume["pistes"].append(creer_resume_piste(fichier, numero_piste))
    fichier.close()
    return resume

def lire_header(fichier, resume):
    utils.verifier(fichier, b'MThd', "Ce n'est pas un fichier Midi")
    taille_header = utils.lire_entier(fichier, 4) 
    resume["format"] = utils.lire_entier(fichier, 2)
    resume["nb_pistes"] = utils.lire_entier(fichier, 2)
    verifier_format(resume) # test d'erreurs
    resume["tempo"] = lire_tempo(fichier)
    utils.avancer(fichier, taille_header - 6) # ces octets sont reserves aux constructeurs MIDI        

def verifier_format(resume):
    if resume["format"] > 2:
        raise ValueError("Format MIDI inconnu.")
    if resume["format"] == 0 and resume["nb_pistes"] != 1:
        raise ValueError("Le nombre de pistes ne correspond pas au format MIDO 0")

def lire_tempo(fichier):
    octet1 = ord(fichier.read(1))
    octet2 = ord(fichier.read(1))
    if octet1 < 128: # bit de poids fort = 0
        return {"metrique" : True, "valeur" : 256 * octet1 + octet2}
    else: ### Dans ce cas pas compris comment s'en servir (pas de fichier exemple)
        return {"metrique" : False, "smpte" : octet1 - 128, "tpf" : octet2}

def creer_resume_piste(fichier, num_piste):
    utils.verifier(fichier, b'MTrk', "Ce n'est pas le début d'une piste")
    taille_piste = utils.lire_entier(fichier, 4)
    position = fichier.tell() #retourne le nombre d'octets passé depuis le début
    utils.avancer(fichier, taille_piste - 3) # -3 pour verifier le meta "fin de piste"
    utils.verifier(fichier, b'\xFF\x2F\x00', "Ce n'est pas la fin d'une piste")
    return {'id' : num_piste, 'début' : position, 'fin' : position + taille_piste}

if __name__ == "__main__":
    # suivant l'environnement, peut avoir besoin de mettre un chemin different
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    print(creer_resume(nom_fichier))

