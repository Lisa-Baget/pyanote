#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.midi.controleur

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de jouer un album en utilisant un controleur.

TODO: Tester le controleur dans un thread, enrichier le controleur
"""
import time
import pyanote.son as son
import pyanote.album as alb
import pyanote.test_controleur_vers_interface as ci

def creer_controleur(nom_fichier, sortie_midi, widget=False, karaoke=True):
    album = alb.creer_album(nom_fichier)
    controleur = {"fichier": nom_fichier, "midi": sortie_midi, "widget": widget, "chansons": album["chansons"]}
    controleur["nom"] = nom_fichier.split('/')[-1] # decoupe le chemin, le dernier c'est le nom du fichier
    controleur["ticks/beat"] = initialiser_tempo(album["tempo"]) ## peut faire une erreur si tempo de type 2
    controleur["micros/tick"] = maj_tempo(controleur, (60 / 120) * 10**6) # valeur par defaut, 120BPM -> 500000 microsecondes/beat
    controleur["vitesse"] = 1 ## pour controler vitesse de lecture
    controleur["pistes actives"] = [True] * album['nb_pistes']
    initialiser_controleur(controleur)
    controleur["notes actives"] = initialiser_notes_actives()
    controleur["analyse"] = False
    controleur["canaux libres"] = [True] * 16
    controleur['kar'] = karaoke and controleur["nom"][-3:] == 'kar' # vrai si j'ai dit vrai et que c'est un fichier kar
    controleur['texte karaoke'] = []
    return controleur

def initialiser_tempo(dico_tempo):
    if dico_tempo["metrique"]: # le seul cas qu'on sait faire
        return dico_tempo["valeur"] # recuperation du ticks/beat, plus besoin du resume
    else:
        raise TypeError("Ce type de tempo n'est pas encore traité")

def initialiser_controleur(controleur):
    controleur["titre"] = 0
    controleur["evenement"] = 0
    controleur["temps_ticks"] = 0
    controleur["temps_micros"] =  0
    controleur["seconde_transmise"] = 0
    controleur["fin"] = False
    controleur["pause"] = False

def initialiser_notes_actives():
    notes_actives = []
    for i in range(16): # pour chaque canal
        notes_actives.append(set([]))
    return notes_actives


def maj_tempo(controleur, tempo):
    ### le ticks/beat dans le controleur est ce qui a été lu dans le header
    ### le tempo envoyé par les messages meta est en microsecondes/beat
    return tempo / controleur["ticks/beat"] # Le retour est en microsecondes / tick 

def maj_temps(controleur, ticks):
    controleur["temps_ticks"] += ticks
    micros = ticks * controleur["micros/tick"]
    controleur["temps_micros"] += micros
    secondes = controleur["temps_micros"] // 10**6
    if controleur['widget'] and secondes > controleur["seconde_transmise"]:
        controleur["seconde_transmise"] = secondes
        controleur['widget'].after(0, ci.maj_temps, controleur['widget'], secondes)
    return micros

def maj_note_active(message, controleur):
    if message[0] // 16 == 8: # note off
        controleur["notes actives"][message[0] % 16].discard(message[1])
    elif message[0] // 16 == 9: # vrai note on (on a enlevé les faux notes on dans piste.py)
        canal = message[0] % 16
        if canal != 9: # on n'a pas besoin d'arreter les notes du canal batterie
            controleur['canaux libres'][canal] = False
            controleur["notes actives"][canal].add(message[1])

def jouer_album(controleur):
    album = controleur["chansons"]
    while (not controleur['fin']):
        if controleur['pause']:
            vider_notes_actives(controleur)
            time.sleep(0.1) # durée à verifier dans tests
        else: # traiter le prochain evenement
            evenement = album[controleur["titre"]][controleur["evenement"]]
            micros = maj_temps(controleur, evenement[0])
            if not controleur['analyse']:
                time.sleep((micros / 10**6) / controleur["vitesse"] )
            traiter_message(evenement[2], evenement[1], controleur)
            maj_evenement(album, controleur)
    vider_notes_actives(controleur)

def traiter_message(message, num_piste, controleur):
    if len(message) == 1: # systeme
        son.message_systeme(controleur['midi'], message)
    elif len(message) == 3: # controle
        maj_note_active(message, controleur)
        if controleur['pistes actives'][num_piste]: # si on doit jouer un message de cette piste
            son.message_controle(controleur['midi'], message)
    else: # meta
        if message[0] == 1 and controleur['kar']: ### karaoke
            controleur['texte karaoke'].append(message[1])
            if not controleur['analyse']:
                print(message[1], end='')
        elif message[0] == 81: # changement tempo
            maj_tempo(controleur, message[1])

def maj_evenement(album, controleur):
    if controleur["evenement"] + 1 == len(album[controleur["titre"]]): # on a traité le dernier evenement de la piste
        if controleur["titre"] + 1 == len(album): # on a traité la dernière piste
            controleur["fin"] = True ## faudrait peut etre prevoir une lecture en boucle
        else:
            controleur["titre"] += 1 # piste suivante
            controleur["evenement"] = 0
    else: # continuer sur la même piste
        controleur["evenement"] += 1  

def vider_notes_actives(controleur):
    for i in range(16):
        for note in controleur['notes actives'][i]:
            son.message_controle(controleur['midi'], [128 + i, note, 0])
        controleur['notes actives'][i] = set([])

if __name__ == "__main__":
    import tkinter
    from tkinter.filedialog import askopenfilename
    root = tkinter.Tk()
    root.withdraw() # https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
    nom_fichier = askopenfilename()
    son_midi = son.connecter_sortie()
    controleur = creer_controleur(nom_fichier, son_midi)
    jouer_album(controleur)
    son.deconnecter(son_midi)

