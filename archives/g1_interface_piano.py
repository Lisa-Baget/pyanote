#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""g1_interface_piano

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Interface graphique pour pouvoir jouer du piano.

TO DO: jouer avec les touches du clavier, rajouter des boutons de controle (canal, instrument, ...)
"""

import tkinter as tk
import pyanote.son as son
import pyanote.accords as accords
import pyanote.notes as notes

def creer_piano(maitre, midi, canal, octave_debut, nb_octaves, w_touche=20, h_touche=100, couleurs=["ivory", "ghostwhite", "black", "gray", "lightgray", "silver"]):
    canvas = tk.Canvas(maitre, width = 7 * nb_octaves * w_touche, height = h_touche)
    canvas.touches = {} # le piano va avoir un dictionnaire {note: touche} pour pouvoir lui dire de changer l'apparence d'une touche en fonction de la note
    canvas.midi = midi
    canvas.canal = canal
    canvas.accord = "aucun"
    for i in range(nb_octaves):
            creer_octave(canvas, 12 * (i + octave_debut + 1), i * w_touche * 7, w_touche, h_touche, couleurs)
    return canvas

def creer_octave(canvas, note_debut, w_base, w_touche, h_touche, couleurs):
    notes = [0, 2, 4, 5, 7, 9, 11]
    for i in range(len(notes)): # dessin des blanches
        note = note_debut + notes[i]
        canvas.touches[note] = creer_touche(canvas, w_base + i*w_touche, w_touche, h_touche, couleurs[0], couleurs[1], couleurs[4], note)
    for i in range(len(notes) - 1): # dessin des noires
        if (notes[i+1] - notes[i]) == 2: # il y a bien un diese ici
            note = note_debut + 1 + notes[i]
            canvas.touches[note] = creer_touche(canvas, w_base + i*w_touche + 0.65*w_touche, 0.7*w_touche, 0.6*h_touche, couleurs[2], couleurs[3], couleurs[5], note)

def creer_touche(canvas, w_base, w_touche, h_touche, couleur1, couleur2, couleur3, note):
    touche = tk.Canvas(canvas, width=w_touche, height=h_touche, background=couleur1)
    touche.note, touche.couleur1, touche.couleur2 = note, couleur1, couleur2
    touche.parent = canvas
    touche.texte = touche.create_text(w_touche / 2, h_touche-10, text=notes.nombre_vers_note(note), fill=couleur3, state="hidden")
    touche.pressee = False ### AJOUT KP
    touche.place(x=w_base, y=0)
    touche.bind("<Button-1>", appuyer_touche)
    touche.bind("<ButtonRelease-1>", relacher_touche) ### AJOUT KP
    touche.bind("<Leave>", relacher_touche) ### AJOUT KP
    return touche

def appuyer_touche(evenement):
    touche = evenement.widget
    accord = accords.construire_accord(touche.note, touche.parent.accord)
    touche.pressee = accord ### AJOUT KP
    for note in accord:
        colorer_touche(touche.parent, note)
        message = [0x90 + touche.parent.canal, note, 255]
        son.message_controle(touche.parent.midi, message)
    ##evenement.widget.after(500, relacher_touche, touche.parent, accord) ## RETRAIT KP

def relacher_touche(evenement):
    touche = evenement.widget
    if touche.pressee:
        accord = touche.pressee
        touche.pressee = False
        for note in accord:
            retablir_touche(evenement.widget.master, note)
        evenement.widget.after(500, fin_relacher_touche, touche.parent, accord)

def fin_relacher_touche(piano, accord):
    for note in accord:
        message = [0x80 + piano.canal, note, 255]
        son.message_controle(piano.midi, message)

def colorer_touche(piano, note):
    try:
        touche = piano.touches[note]
        touche.configure(bg = touche.couleur2)
        montrer_texte(piano, note)
    except KeyError:
        pass

def retablir_touche(piano, note):
    try:
        touche = piano.touches[note]
        touche.configure(bg = touche.couleur1)
        cacher_texte(piano, note)
    except KeyError:
        pass

def cacher_texte(piano, note):
    try:
        touche = piano.touches[note]
        touche.itemconfigure(touche.texte, state = "hidden")
    except KeyError:
        pass

def montrer_texte(piano, note):
    try:
        touche = piano.touches[note]
        touche.itemconfigure(touche.texte, state = "disabled")
    except KeyError:
        pass

def quitter(fenetre, midi):
    son.deconnecter(midi)
    fenetre.destroy()

if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("py@Note")
    midi = son.connecter_sortie()
    canal = 8
    piano = creer_piano(fenetre, midi, canal, 3, 5, 40, 180)
    piano.pack()
    piano.accord = "aucun"
    fenetre.wm_protocol('WM_DELETE_WINDOW', lambda: quitter(fenetre, midi))
    fenetre.mainloop()