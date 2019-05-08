#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.thread

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de controler la lecture d'un fichier Midi.
"""
import pyanote.resume as res
import pyanote.album as alb
import pyanote.son as son
import pyanote.controleur as cont
import threading


def preparer_lecture(nom_fichier):
    resume = res.creer_resume(nom_fichier)
    album = alb.creer_album(resume)
    midi = son.connecter_sortie()
    controleur = cont.creer_controleur(resume, midi)
    controleur["thread"] = threading.Thread(None, cont.jouer_album, None, [album, controleur])
    return controleur

def demarrer_lecture(controleur):
    controleur["thread"].start()

def pause_lecture(controleur):
    controleur["pause"] = True

def reprendre_lecture(controleur):
    controleur["pause"] = False

def arreter_lecture(controleur):
    controleur["fin"] = True


if __name__ == "__main__":
    import time
    import tkinter
    from tkinter.filedialog import askopenfilename
    root = tkinter.Tk()
    root.withdraw() # https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
    nom_fichier = askopenfilename()
    controleur = preparer_lecture(nom_fichier)
    demarrer_lecture(controleur)
    time.sleep(10)
    pause_lecture(controleur)
    time.sleep(5)
    reprendre_lecture(controleur)
    time.sleep(10)
    arreter_lecture(controleur)





