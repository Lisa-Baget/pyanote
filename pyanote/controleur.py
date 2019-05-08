#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.midi.controleur

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de jouer un album en utilisant un controleur.

TODO: Tester le controleur dans un thread, enrichier le controleur
"""
import time
import pyanote.son as son

def creer_controleur(resume, sortie_midi):
    controleur = {"titre": 0, "evenement": 0, "temps_ticks": 0, "temps_micros": 0,
                  "pause": False, "fin": False, "midi": sortie_midi}
    if resume["tempo"]["metrique"]:
        controleur["ticks/beat"] = resume["tempo"]["valeur"]
        maj_tempo(controleur, 500000) # valeur par defaut, 120BPM
    else:
        raise TypeError("Ce type de tempo n'est pas encore traité")
    return controleur

def maj_tempo(controleur, tempo):
    print('changement tempo')
    controleur["micros/tick"] = tempo / controleur["ticks/beat"]

def maj_temps(controleur, ticks):
    controleur["temps_ticks"] += ticks
    micros = ticks * controleur["micros/tick"]
    controleur["temps_micros"] += micros
    return micros

def jouer_album(album, controleur):
    while (not controleur['fin']):
        if controleur['pause']:
            time.sleep(0.1) # durée à verifier dans tests
        else: # traiter le prochain evenement
            evenement = album[controleur["titre"]][controleur["evenement"]]
            micros = maj_temps(controleur, evenement[0])
            time.sleep(micros / 10**6)
            traiter_message(evenement[1], evenement[2], controleur)
            maj_evenement(album, controleur)

def traiter_message(message, num_piste, controleur):
    if len(message) == 1: # systeme
        son.message_systeme(controleur['midi'], message)
    elif len(message) == 3: # controle
        son.message_controle(controleur['midi'], message)
    else: # meta
        if message[0] == 1: ### karaoke
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

