#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""l1_lecteur_basique

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Fonction la plus simple possible pour jouer un album. Utilise les modules pyanote.album
et pyanote.son.
"""
import pyanote.album as alb
import pyanote.son as son
import time

def jouer_album(nom_fichier):
    album = alb.creer_album(nom_fichier)
    maj_tempo(album, 500000) ## 500000 micros/noire correspond à 120bpm (noire/minute)
    album['midi'] = son.connecter_sortie()
    for chanson in album['chansons']:
        for evenement in chanson:
            time.sleep(evenement[0] * album['micros/tick'] / 10**6)
            message = evenement[2]
            traiter_message(message, album)
    son.deconnecter(album['midi'])

def maj_tempo(album, micros_par_noire):
    ### le ticks/beat dans l'album est ce qui a été lu dans le header
    ### le tempo envoyé par les messages meta est en microsecondes/noire
    album['micros/tick'] =  micros_par_noire / album["ticks/noire"] # Le retour est en microsecondes / tick 

def traiter_message(message, album):
    if len(message) == 1: # systeme
        son.message_systeme(album['midi'], message)
    elif len(message) == 3: # controle
        son.message_controle(album['midi'], message)
    elif message[0] == 81: ## changement tempo
        maj_tempo(album, message[1]) 

if __name__ == "__main__":
    jouer_album("fichiersMidi/New Order - Blue Monday.mid")