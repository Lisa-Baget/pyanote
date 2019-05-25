"""pyanote.piano

(C) Lisa Baget, 2018-2019

Ce module contient les fonctions permettant construire un piano qui est consreuit
a partir d'un piano et d'un ensemble de touches de controles.
"""
import tkinter as tk
import pyanote.notes
import pyanote.son
import pyanote.clavier as pycl
import pyanote.instruments as inst
import pyanote.accords as pyacc
import math

MINVOLUME = 133 ## si le volume est au dessous de 133 on n'entend plus rien

def creer_piano(contenant, sortie_midi, octave_debut, nb_octaves, params):
    w_piano = params['blanche']['w'] * 7 * nb_octaves
    piano = tk.Canvas(contenant, width = w_piano, height = params['blanche']['h'] + 46)
    piano.octave_debut = octave_debut
    piano.clavier = pycl.creer_clavier(piano, sortie_midi, octave_debut, nb_octaves, params)
    piano.clavier.place(x = 0, y = 48)
    piano.controles = creer_controles(piano, nb_octaves, w_piano)
    piano.controles.place(x=0, y=0)
    changer_apparence_controles(piano)
    return piano

def creer_controles(piano, nb_octaves, w_piano):
    controles = tk.Canvas(piano, width = w_piano, height = 48)
    police_label = ('comic sans ms', 8, 'italic')
    piano.canal = creer_controle_canal(piano, controles)
    piano.canal.place(x = 10, y=7)
    piano.famille = creer_controle_famille(piano, controles)
    piano.famille.place(x = 60, y=7)
    piano.instrument = creer_controle_instrument(piano, controles)
    piano.instrument.place(x = 275, y=7)
    piano.volume = creer_controle_volume(piano, controles)
    piano.volume.place(x = 580, y=7)
    piano.accords = creer_controle_accords(piano, controles)
    piano.accords.place(x = 655, y=7)
    piano.octave = creer_controle_octave(piano, controles, nb_octaves)
    piano.octave.place(x = 870, y=7)
    for texte, position in [["canal", 10], ["famille", 60], ["instrument", 275], ["volume", 580],["accords", 655], ["octave", 870]]:
        label = tk.Label(controles, text = texte, fg = "silver", bg = "black", font = police_label)
        label.place(x = position, y=28)
    return controles

def initialiser_controles(piano):
    changement_canal(piano)
    changement_instrument(piano)
    changement_volume(piano)

def changer_apparence_controles(piano):
    piano.controles.configure(bg = 'black')
    police = ('Digital-7 Mono', 12, 'bold')
    for spinbox in [piano.canal, piano.famille, piano.instrument, piano.volume, piano.accords, piano.octave]:
        spinbox.configure(readonlybackground="darkslategrey", buttonbackground='black', fg='lime', font=police, justify="center")

def creer_controle_canal(piano, controles):
    canaux_libres = ['{:02}'.format(i) for i in range(16)]
    canal = tk.Spinbox(controles, values=canaux_libres, width=3, wrap=True, state='readonly')
    canal.configure(command = lambda: changement_canal(piano))
    return canal

def changement_canal(piano):
    piano.clavier.canal = int(piano.canal.get())

def creer_controle_famille(piano, controles):
    famille = tk.Spinbox(controles, values=list(inst.INSTRUMENTS), width=21, wrap=True, state='readonly')
    famille.configure(command = lambda: changement_famille(piano))
    return famille

def changement_famille(piano):
    piano.instrument.configure(values = list(inst.INSTRUMENTS[piano.famille.get()]))
    changement_instrument(piano)

def creer_controle_instrument(piano, controles):
    instrument = tk.Spinbox(controles, values=list(inst.INSTRUMENTS[piano.famille.get()]), width=30, wrap=True, state='readonly')
    instrument.configure(command = lambda: changement_instrument(piano))
    return instrument

def changement_instrument(piano):
    instrument = inst.INSTRUMENTS[piano.famille.get()][piano.instrument.get()]
    pyanote.son.message_controle(piano.clavier.midi, [0xC0 + piano.clavier.canal, instrument, 0])

def creer_controle_volume(piano, controles):
    pourcentages = ['{:03}'.format(i) for i in range(101)] # formule magique !
    volume_initial = tk.StringVar() # https://stackoverflow.com/questions/32145376/how-can-i-establish-a-default-string-value-on-a-tkinter-spinbox
    volume = tk.Spinbox(controles, values=pourcentages, textvar = volume_initial, width=4, state='readonly')
    volume_initial.set("050")
    volume.configure(command = lambda: changement_volume(piano))
    return volume

def changement_volume(piano):
    volume = math.floor(int(piano.volume.get()) * ((255 - MINVOLUME) / 100) + MINVOLUME)
    piano.clavier.volume = volume

def creer_controle_accords(piano, controles):
    valeurs = list(pyacc.ACCORDS)
    accords = tk.Spinbox(controles, values=valeurs, width=20, state='readonly', wrap = True)
    accords.configure(command = lambda: changement_accords(piano))
    return accords

def changement_accords(piano):
    piano.clavier.accord = piano.accords.get()

def creer_controle_octave(piano, controles, nb_octaves):
    valeurs = []
    for i in range(piano.octave_debut, piano.octave_debut + nb_octaves):
        valeurs.append(str(i))
    octave = tk.Spinbox(piano, values = valeurs, width=2, state='readonly', wrap=True)
    octave.configure(command = lambda: changement_octave(piano))
    return octave


def changement_octave(piano):
    octave = int(piano.octave.get()) - piano.octave_debut
    piano.clavier.octaves[octave].focus_set()

if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title = "py@note" 
    sortie_midi = pyanote.son.connecter_sortie()
    params_touches = {
        "blanche": {"w" : 40, "h": 180, "couleur": "ivory", "altcouleur": "ghostwhite", "text": "lightgray"},
        "noire": {"w" : 24, "h": 110, "couleur": "black", "altcouleur": "gray", "text": "silver"}
    }
    piano1 = creer_piano(fenetre, sortie_midi, 3, 5, params_touches)
    piano1.pack()
    fenetre.mainloop()