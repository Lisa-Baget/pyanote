#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.midi.controleur

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de jouer un album en utilisant un controleur.

TODO: Tester le controleur dans un thread, enrichier le controleur
"""
import time
import pyanote.son as son

def creer_controleur(resume, sortie_midi, analyse=False):
    controleur = {"titre": 0, "evenement": 0, "temps_ticks": 0, "temps_micros": 0,
                  "pause": False, "fin": False, "midi": sortie_midi, "notes actives": [],
                  "canaux libres": [True] * 16, "pistes actives": [not analyse] * resume['nb_pistes'], 
                  'analyse': analyse, 'kar': False}
    if resume["tempo"]["metrique"]:
        controleur["ticks/beat"] = resume["tempo"]["valeur"]
        maj_tempo(controleur, 500000) # valeur par defaut, 120BPM
    else:
        raise TypeError("Ce type de tempo n'est pas encore traité")
    for __ in range(16): # pour chaque canal
        controleur["notes actives"].append(set([]))
    if resume['fichier'][-3:] == 'kar':
        controleur['kar'] = True
        controleur['texte karaoke'] = []
    return controleur

def maj_tempo(controleur, tempo):
    controleur["micros/tick"] = tempo / controleur["ticks/beat"]

def maj_temps(controleur, ticks):
    controleur["temps_ticks"] += ticks
    micros = ticks * controleur["micros/tick"]
    controleur["temps_micros"] += micros
    return micros

def maj_note_active(message, controleur):
    if message[0] // 16 == 8 or (message[0] // 16 == 9 and message[2] == 3): # note off
        controleur["notes actives"][message[0] % 16].discard(message[1])
    elif message[0] // 16 == 9: # vrai note on
        canal = message[0] % 16
        if canal != 9: # on n'a pas besoin d'arreter les notes du canal batterie
            controleur['canaux libres'][canal] = False
            controleur["notes actives"][canal].add(message[1])

def jouer_album(album, controleur):
    while (not controleur['fin']):
        if controleur['pause']:
            vider_notes_actives(controleur)
            time.sleep(0.1) # durée à verifier dans tests
        else: # traiter le prochain evenement
            evenement = album[controleur["titre"]][controleur["evenement"]]
            micros = maj_temps(controleur, evenement[0])
            if not controleur['analyse']:
                time.sleep(micros / 10**6)
            traiter_message(evenement[1], evenement[2], controleur)
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
            controleur["fin"] = True
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
    import pyanote.resume as res
    import pyanote.album as alb
    import tkinter
    from tkinter.filedialog import askopenfilename
    root = tkinter.Tk()
    root.withdraw() # https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
    nom_fichier = askopenfilename()
    resume = res.creer_resume(nom_fichier)
    album = alb.creer_album(resume)
    son_midi = son.connecter_sortie()
    controleur = creer_controleur(resume, son_midi)
    jouer_album(album, controleur)
    son.deconnecter(son_midi)

