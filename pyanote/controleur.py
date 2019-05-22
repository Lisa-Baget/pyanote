#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.controleur

(C) Lisa Baget, 2018-2019

Ce module contient les fonctions permettant construire un controleur qui va gerer la lecture d'un
fichier MIDI.
"""
import pyanote.album as alb
import pyanote.modificateurs as mod
import threading
import time

CONTROLEUR_STANDARD = {
    'index_chanson' : 0, ## le numero de la chanson qu'on est en train de jouer
    'index_evenement' : 0, ## Le numero de l'evenement dans la chanson qu'on est en train de jouer
    'vitesse' : 1, # 1 standard (vitesse normale), float('inf') pour ne plus faire de sleep
    'fin' : False, ## le mettre à True pour finir la lecture
    'pause' : False ## le mettre à True pour mettre la lecture en pause
}

def creer_controleur(nom_fichier, **params):
    controleur = alb.creer_album(nom_fichier) ## le controleur est d'abord un album 
    reinitialiser_controleur(controleur)
    mod.initialiser_modificateurs(controleur) ## faire tous les ajouts prévus dans modificateurs.py
    mod.preparer_modificateurs(controleur, **params)
    return controleur

def reinitialiser_controleur(controleur):
    controleur.update(CONTROLEUR_STANDARD) ## on lui rajoute toutes les clés/valeurs du controleur standard et on remplace si deja la
    controleur["micros/tick"] = maj_tempo(controleur)
    mod.reinitialiser_modificateurs(controleur)
   
def maj_tempo(controleur, tempo = 500000): # valeur par defaut, 120BPM -> (60/120) * 10**6 =  500000 microsecondes/beat
    ### le ticks/beat dans le controleur est ce qui a été lu dans le header
    ### le tempo envoyé par les messages meta est en microsecondes/beat
    return tempo / controleur["ticks/noire"] # Le retour est en microsecondes / tick

def demarrer(controleur, thread = False):
    mod.preparer_modificateurs(controleur)
    if thread:
        controleur['thread'] = threading.Thread(None, boucle_lecture, None, [controleur])
        controleur['thread'].start()
    else:
        boucle_lecture(controleur)

def boucle_lecture(controleur):
    while not controleur['fin']: # tant que le controleur ne dit pas que c'est fini
        if controleur['pause']: # si le controleur est en pause
            mod.executer_modificateurs_pause(controleur)
            time.sleep(0.1) # durée à verifier dans tests, on fait un sleep pour pas retester la pause immediatement
        else: # traiter le prochain evenement
            evenement = evenement_courant(controleur)
            traiter_evenement(controleur, evenement)
            prochain_evenement(controleur)
    mod.executer_modificateurs_arret(controleur)

def evenement_courant(controleur):
    ''' Retourne l'evenement qui doit etre joué par le controleur.
    '''
    chansons = controleur['chansons']
    numero_chanson = controleur["index_chanson"]
    numero_evenement = controleur["index_evenement"]
    return chansons[numero_chanson][numero_evenement]

def prochain_evenement(controleur):
    ''' Mise a jour du controleur pour qu'il indique le prochain evenement courant.
    '''
    chansons = controleur['chansons']
    numero_chanson = controleur['index_chanson']
    chanson = chansons[numero_chanson]
    if controleur["index_evenement"] + 1 == len(chanson): # on a traité le dernier evenement de la chanson
        prochaine_chanson(controleur)
    else: # continuer sur la même piste
        controleur["index_evenement"] += 1

def prochaine_chanson(controleur):
    mod.executer_modificateurs_fin_chanson(controleur)
    chansons = controleur['chansons']
    if controleur["index_chanson"] + 1 == len(chansons): # on a traité la dernière chanson
        mod.executer_modificateurs_fin_album(controleur)
        controleur["fin"] = True ## c'est la fin
    else: # on  doit passer à la chanson suivante
        controleur["index_chanson"] += 1 # chanson suivante
        controleur["index_evenement"] = 0

def traiter_evenement(controleur, evenement):
    traiter_delta_temps(controleur, evenement[0])
    traiter_message(controleur, evenement[1], evenement[2])

def traiter_delta_temps(controleur, ticks):
    micros = ticks * controleur["micros/tick"]
    mod.executer_modificateurs_delta_temps(controleur, ticks, micros)
    time.sleep(micros / (10**6 * controleur["vitesse"]))

def traiter_message(controleur, num_piste, message):
    if len(message) == 1: # systeme
        mod.executer_modificateurs_message_systeme(controleur, num_piste, message)
    elif len(message) == 3: # controle
        mod.executer_modificateurs_message_controle(controleur, num_piste, message)
    else: # meta
        mod.executer_modificateurs_message_meta(controleur, num_piste, message)
        if message[0] == 0x51: # changement tempo
            controleur["micros/tick"] = maj_tempo(controleur, message[1])

if __name__ == "__main__":
    import tkinter
    from tkinter.filedialog import askopenfilename
    import pyanote.son as son
    nom_fichier = 'fichiersMidi/Madness - Baggy Trousers.kar'
    sortie_son = son.connecter_sortie()
    s1 = time.time()
    controleur = creer_controleur(nom_fichier, midi = sortie_son)
    #mod.preparer_modificateurs(controleur, midi = sortie_son)
    s2 = time.time()
    print("Temps écoulé par la creation du controleur:", s2 - s1)
    controleur['vitesse'] = float('inf')
    t1 = time.time()
    demarrer(controleur)
    t2 = time.time()
    print("Temps écoulé par la lecture vitesse infinie:", t2 - t1)
    reinitialiser_controleur(controleur)
    demarrer(controleur, True)
    
    ### Résultats de vieux tests
    ### Avec modificateurs vides
    ### Temps écoulé par la creation du controleur: 0.04002785682678223
    ### Temps écoulé par la lecture vitesse infinie: 0.0190122127532959