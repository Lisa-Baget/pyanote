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
    '''
    piste = []
    fichier = open(resume["fichier"], 'rb')
    resume_piste = resume['pistes'][num_piste]
    utils.avancer(fichier, resume_piste['début'])
    # Le mécanisme de sauvegarde est pour le RUNNING STATUS dans la specification.
    # Bonne explications dans http://www.gweep.net/~prefect/eng/reference/protocol/midispec.html
    sauvegarde = [None] # initialisation de la sauvegarde. liste car mutable 
    while fichier.tell() < resume_piste['fin']:
        piste.append(lire_evenement(fichier, num_piste, sauvegarde)) 
    return piste

def lire_evenement(fichier, num_piste, sauvegarde):
    ''' Retourne le prochain évènement de la piste num_piste lu dans le fichier.

        Cet évènement est une liste de la forme [delta_temps, message, num_piste].

    Le delta_temps (temps depuis le dernier evenement) est exprimé en ticks. 
    Sa valeur en secondes dépend du header et des messages de changement de tempo.
    '''
    delta_temps = utils.lire_entier_variable(fichier) 
    message = lire_message(fichier, sauvegarde)
    return [delta_temps, message, num_piste]

def lire_message(fichier,sauvegarde):
    ''' Retourne le prochain message lu dans le fichier.

        Un message est toujours une liste. La longueur de cette liste est 1 pour les messages
        systemes, 2 pour les messages meta et 3 pour les messages de controle.
    '''
    status = fichier.read(1)
    if status == b'\xFF': # Meta
        # il faudra enlever la ligne suivante si on trouve un fichier MIDI qui fait une
        # erreur "Sauvegarde introuvable" et qui marche avec un vrai lecteur MIDI
        sauvegarde[0] = None # annule la sauvegarde ??? Pas sur, infos contradictoires.
        return lire_message_meta(fichier)
    elif status == b'\xF0' or status == b'\xF7': # Systeme
        sauvegarde[0]= None # annule la sauvegarde (la c'est sur)
        return lire_message_systeme(fichier, status)
    else: # Controle
        return lire_message_controle(fichier, status, sauvegarde)

def lire_message_systeme(fichier, octet): # liste de longueur 1
    ''' Retourne une liste [chaine_binaire]
    '''
    taille = utils.lire_entier_variable(fichier)
    valeur = fichier.read(taille)
    return [octet + valeur]

def lire_message_meta(fichier): # liste de longueur 2
    ''' Retourne une liste [type, valeur]. Ce qui est stocké dans la valeur dépend du type.
    '''
    type_meta = ord(fichier.read(1))
    taille = utils.lire_entier_variable(fichier)
    if type_meta == 0x01: # texte sans format defini
        ### Rajouter des formats si des fichiers Karaoke marchent vraiment pas...
        valeur = utils.lire_chaine(fichier, taille, ['ascii', 'utf-8', 'latin-1']) # essai plusieurs format car on sait pas
    elif type_meta >= 0x02 and type_meta <= 0x07: # texte
        valeur = utils.lire_chaine(fichier, taille, ['ascii']) # la le format MIDI impose ascii
    elif type_meta in [0x00, 0x20, 0x51]: # entier
        valeur = utils.lire_entier(fichier, taille)
    elif type_meta in [0x2F, 0x54, 0x58, 0x59]: # liste d'octets
        valeur = utils.lire_liste_octets(fichier, taille)
    else:
        valeur = fichier.read(taille) ### si on sait pas ce sera du binaire...
    return [type_meta, valeur]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def lire_message_controle(fichier, status, sauvegarde): # liste de longueur 3
    ''' Retourne un message de controle de la forme [status, arg1, arg2].

    Les 4 premiers bits du status (status // 16) codent l'instruction et les 4
    derniers (status % 16) le canal.

    Pour les instructions à 1 argument, on impose ici arg2 = 0.
    '''
    octet = ord(status)
    instruction = octet // 16 # 4 1ers bits
    if instruction < 8 or instruction > 14: # pas une instruction, utilisation de la sauvegarde
        if sauvegarde[0] != None: # il y a une sauvegarde
            octet, arg1 = sauvegarde[0], octet
        else: # on aurait du trouver la sauvegarde
            raise SyntaxError("Sauvegarde introuvable")
    else: # le status code bien une nouvelle instruction
        sauvegarde[0] = octet # mise a jour de la sauvegarde
        arg1 = ord(fichier.read(1))
    if instruction == 12 or instruction ==13: # instructions à 1 argument
        arg2 = 0
    else: # instructions à deux arguments
        arg2 = ord(fichier.read(1))
    return [octet, arg1, arg2]

if __name__ == "__main__":
    import pyanote.resume as res
    # suivant l'environnement, peut avoir besoin de mettre un chemin different
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    resume = res.creer_resume(nom_fichier)
    print("==========================================")
    print("Exemples de pistes MIDI")
    print("==========================================")
    print('------------------------------------------')
    print('* Piste 0')
    print('------------------------------------------')
    print(creer_piste(resume, 0))
    print('------------------------------------------')
    print('* Piste 1 (20 premiers evenements)')
    print('------------------------------------------')
    print(creer_piste(resume, 2)[0:20])
    