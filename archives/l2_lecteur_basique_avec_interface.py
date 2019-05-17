#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""l2_lecteur_basique_avec_interface

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Essai pour utiliser les fonctions basiques de lecture depuis une interface tkinter.

Ca ne marche pas car des que la fonction jouer_album se lance, tout est gelé et tkinter
n'a plus la main pour detecter si on veut faire autre chose. Il faut donc trouver une autre idée.
"""
import pyanote.album as alb
import pyanote.son as son
import time

def jouer_album(nom_fichier):
    album = alb.creer_album(nom_fichier)
    album['micros/tick'] = maj_tempo(album, 500000) ## 500000 micros/noire correspond à 120bpm (noire/minute)
    album['midi'] = son.connecter_sortie()
    for chanson in album['chansons']:
        for evenement in chanson:
            time.sleep(evenement[0] * album['micros/tick'] / 10**6)
            message = evenement[2]
            traiter_message(message, album)
    son.deconnecter(album['midi'])

def maj_tempo(controleur, tempo):
    ### le ticks/beat dans le controleur est ce qui a été lu dans le header
    ### le tempo envoyé par les messages meta est en microsecondes/noire
    return tempo / controleur["ticks/noire"] # Le retour est en microsecondes / tick 

def traiter_message(message, album):
    if len(message) == 1: # systeme
        son.message_systeme(album['midi'], message)
    elif len(message) == 3: # controle
        son.message_controle(album['midi'], message)
    elif message[0] == 81: ## changement tempo
        maj_tempo(album, message[1]) 

if __name__ == "__main__":
    import tkinter
    nom_fichier = "fichiersMidi/New Order - Blue Monday.mid"
    fenetre = tkinter.Tk()
    barre_menu = tkinter.Menu(fenetre)
    menufichier = tkinter.Menu(barre_menu,tearoff=0)
    menufichier.add_command(label="Ouvrir", command = lambda: jouer_album(nom_fichier))
    menufichier.add_command(label="Quitter",command = fenetre.destroy)
    barre_menu.add_cascade(label="Fichier", menu=menufichier)
    fenetre.config(menu=barre_menu)
    fenetre.mainloop()