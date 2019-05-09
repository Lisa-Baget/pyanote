#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.piste

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de construire la liste de tous les évènements contenus
dans une unique piste d'un fichier Midi.
"""
import pyanote.utils as utils


def creer_piste(resume, num_piste):
    ''' Retourne la liste de tous les evenements contenus dans une unique piste du fichier Midi décrit.

    resume: le résumé d'un fichier Midi obtenu par pyanote.midi.fichier.resume.creer_resume(nom_fichier)

    num_piste: le numero de la piste dont on veut les éléments

    Chaque evenement est une liste de la forme [delta_temps, message, num_piste].

    Le delta_temps (temps depuis le dernier evenement) est exprimé en ticks. 
    Sa valeur en secondes dépend du header et des messages de changement de tempo.
    '''
    piste = []
    fichier = open(resume["fichier"], 'rb')
    resume_piste = resume['pistes'][num_piste]
    utils.avancer(fichier, resume_piste['début'])
    sauvegarde = [None] # initialisation de la sauvegarde. liste car mutable 
    while fichier.tell() < resume_piste['fin']:
        delta_temps = utils.lire_entier_variable(fichier) 
        message = lire_message(fichier, sauvegarde)
        piste.append([delta_temps, message, num_piste]) 
    return piste

def lire_message(fichier,sauvegarde):
    status = fichier.read(1)
    if status == b'\xFF': # Meta
        sauvegarde[0] = None # annule la sauvegarde
        return lire_message_meta(fichier)
    elif status == b'\xF0' or status == b'\xF7': # Systeme
        sauvegarde[0]= None # annule la sauvegarde
        return lire_message_systeme(fichier, status)
    else: # Controle
        return lire_message_controle(fichier, status, sauvegarde)

def lire_message_meta(fichier): # liste de longueur 2
    type_meta = ord(fichier.read(1))
    taille = utils.lire_entier_variable(fichier)
    if type_meta == 0x01: # texte sans format defini
        valeur = utils.lire_chaine(fichier, taille, ['ascii', 'utf-8', 'latin-1']) # essai plusieurs format car on sait pas
    elif type_meta >= 0x02 and type_meta <= 0x07: # texte
        valeur = utils.lire_chaine(fichier, taille, ['ascii']) # la le format MIDI impose ascii
    elif type_meta in [0x00, 0x20, 0x51]: # entier
        valeur = utils.lire_entier(fichier, taille)
    elif type_meta in [0x2F, 0x54, 0x58, 0x59]: # liste d'octets
        valeur = utils.lire_liste_octets(fichier, taille)
    else:
        valeur = fichier.read(taille)
    return [type_meta, valeur]

def lire_message_systeme(fichier, octet): # liste de longueur 1
    taille = utils.lire_entier_variable(fichier)
    valeur = fichier.read(taille)
    return [octet + valeur]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def lire_message_controle(fichier, status, sauvegarde): # liste de longueur 3
    octet = ord(status)
    instruction = octet // 16 # 4 1ers bits
    if instruction < 8 or instruction > 14: # pas une instruction
        if sauvegarde[0] != None: # il y a une sauvegarde
            print("sauvegarde utilisée")
            octet, arg1 = sauvegarde[0], octet
        else: # on aurait du trouver la sauvegarde
            print(sauvegarde, status)
            raise SyntaxError("Sauvegarde introuvable")
    else:
        sauvegarde[0] = octet # mise a jour de la sauvegarde
        print("je sauvegarde", octet)
        arg1 = ord(fichier.read(1))
    if instruction == 12 or instruction ==13: # instructions à 1 argument
        arg2 = 0
    else:
        arg2 = ord(fichier.read(1))
    return [octet, arg1, arg2]

if __name__ == "__main__":
    import pyanote.resume as res
    # suivant l'environnement, peut avoir besoin de mettre un chemin different
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    #nom_fichier = 'fichiersMidi/Madness - Baggy Trousers.kar'
    resume = res.creer_resume(nom_fichier)
    print('========= PISTE 0')
    print(creer_piste(resume, 0))
    print('========= PISTE 1 (20 premiers evenements)')
    print(creer_piste(resume, 2)[0:20])
    