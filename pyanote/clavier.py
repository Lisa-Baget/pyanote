#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.clavier

(C) Lisa Baget, 2018-2019

Ce module contient les fonctions permettant construire un clavier (ensemble de touches)
comme une interface graphique Tkinter.
"""
import tkinter as tk
import pyanote.notes
import pyanote.son
import pyanote.accords as pyacc
import pyanote.notes as notes
import time

def creer_clavier(emplacement, sortie_midi, octave_debut, nb_octaves, params, lang =notes.EN):
    largeur_octave = params['blanche']['w'] * 7
    clavier = tk.Canvas(emplacement, width = nb_octaves * largeur_octave, height = params['blanche']['h'])
    clavier.touches, clavier.octaves, clavier.midi = {}, [], sortie_midi
    clavier.accord = 'aucun'
    clavier.lang = lang
    clavier.canal, clavier.volume, clavier.delai_arret = 0, 200, 250
    note_debut = pyanote.notes.note_vers_nombre("C" + str(octave_debut))
    for i in range(nb_octaves):
        creer_octave(clavier, largeur_octave * i, note_debut + i * 12, params)
    clavier.octaves[0].focus_set()
    return clavier

def creer_octave(clavier, x_octave, note_debut, params):
    octave = tk.Canvas(clavier, width = params['blanche']['w'] * 7, height = params['blanche']['h'])
    clavier.octaves.append(octave)
    octave.place(x=x_octave, y=0)
    intervalles = [0, 2, 4, 5, 7, 9, 11]
    for i in range(len(intervalles)):
        creer_touche(octave, note_debut + intervalles[i], i * params['blanche']['w'], params['blanche'])
    for i in range(1, len(intervalles)):
        if intervalles[i] - intervalles[i-1] == 2:
            x = (i * params['blanche']['w']) - (params['noire']['w'] / 2)
            creer_touche(octave, note_debut + intervalles[i] - 1, x, params['noire'])
    construire_racourcis_clavier(octave, note_debut)

def construire_racourcis_clavier(octave, note_debut):
    touches_ordi = ['q', 'z', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h', 'u', 'j']
    octave.notes = {}
    for i in range(len(touches_ordi)):
        octave.notes[touches_ordi[i]] = note_debut + i
        appuie = '<KeyPress-' + touches_ordi[i] + '>'
        relache = '<KeyRelease-' + touches_ordi[i] + '>'
        octave.bind(appuie, appuyer_touche_clavier)
        octave.bind(relache, relacher_touche_clavier)


def creer_touche(octave, note, x, param):
        touche = tk.Canvas(octave, width=param['w'], height=param['h'], bg=param['couleur'])
        clavier = octave.master
        clavier.touches[note] = touche
        touche.place(x=x, y=0)
        touche.note = note
        touche.couleur = param['couleur']
        touche.altcouleur = param['altcouleur']
        nom_note = notes.nombre_vers_note(note, lang = clavier.lang)
        touche.texte = touche.create_text(param['w'] / 2, param['h'] - 10, text = nom_note, fill = param['text'], state = 'hidden')
        touche.appuyee = False
        touche.bind("<Button-1>", appuyer_touche_souris)
        touche.bind("<ButtonRelease-1>", relacher_touche_souris)

def appuyer_touche_souris(evenement):
    appuyer_touche(evenement.widget.master.master, evenement.widget.note)

def appuyer_touche_clavier(evenement):
    ### probleme ici, l'evenement est lancé plein de fois pendant que la touche est appuyée
    ### ca a l'air normal: https://stackoverflow.com/questions/33088597/python-tkinter-keypress-event-trigger-once-hold-vs-pressed
    ### il dit que ce n'est pas un probleme de python, mais de certains claviers (dont le mien apparemment) qui envoie plein de fois
    ### le message keypress tant que la touche reste appuyée. On adapte ici la solution
    clavier = evenement.widget.master
    note = evenement.widget.notes[evenement.char]
    touche = clavier.touches[note]
    if not touche.appuyee:
        appuyer_touche(clavier, note)

def appuyer_touche(clavier, note):
    touche = clavier.touches[note]
    accord = pyacc.construire_accord(note, clavier.accord)
    touche.appuyee = accord
    for note in accord:
        jouer_note(clavier, note)
        colorer_note(clavier, note)

def jouer_note(clavier, note):
	print("Je dois jouer {}".format(note))
	pyanote.son.message_controle(clavier.midi, [0x90 + clavier.canal, note, clavier.volume])

def colorer_note(clavier, note):
    try:
        touche = clavier.touches[note]
        touche.configure(bg = touche.altcouleur)
        touche.itemconfigure(touche.texte, state = "disabled")
    except KeyError:
        pass

def relacher_touche_souris(evenement):
    relacher_touche(evenement.widget.master.master, evenement.widget.note)

def relacher_touche_clavier(evenement):
    relacher_touche(evenement.widget.master, evenement.widget.notes[evenement.char])

def relacher_touche(clavier, note):
    touche = clavier.touches[note]
    accord = touche.appuyee
    touche.appuyee = False
    for note in accord:
        retablir_couleur_note(clavier, note)
        clavier.after(clavier.delai_arret, arreter_note, clavier, note)

def arreter_note(clavier, note):
	pyanote.son.message_controle(clavier.midi, [0x80 + clavier.canal, note, 0])

def retablir_couleur_note(clavier, note):
	try:
		touche = clavier.touches[note]
		touche.configure(bg = touche.couleur)
		touche.itemconfigure(touche.texte, state = "hidden")
	except KeyError:
		pass
    




if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title = "py@note" 
    sortie_midi = pyanote.son.connecter_sortie()
    params_touches = {
        "blanche": {"w" : 30, "h": 100, "couleur": "ivory", "altcouleur": "ghostwhite", "text": "lightgray"},
        "noire": {"w" : 20, "h": 60, "couleur": "black", "altcouleur": "gray", "text": "silver"}
    }
    clavier = creer_clavier(fenetre, sortie_midi, 3, 3, params_touches, lang = notes.FR)
    clavier.pack()
    fenetre.mainloop()

