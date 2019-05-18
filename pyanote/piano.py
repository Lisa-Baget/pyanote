import tkinter as tk
import pyanote.notes
import pyanote.son
import pyanote.clavier as pycl
import pyanote.instruments as inst
import math

MINVOLUME = 133 ## si le volume est au dessous de 133 on n'entend plus rien

def creer_piano(contenant, sortie_midi, octave_debut, nb_octaves, params):
    piano = tk.Canvas(contenant, width = params['blanche']['w'] * 7 * nb_octaves, height = params['blanche']['h'] + 30)
    piano.clavier = pycl.creer_clavier(piano, sortie_midi, octave_debut, nb_octaves, params)
    piano.clavier.place(x = 0, y = 30)
    ## Widget de changement de canal
    canaux_libres = [str(i) for i in range(16)]
    piano.canal = tk.Spinbox(piano, values=canaux_libres, width=2, wrap=True, state='readonly')
    piano.canal.configure(command = lambda: changement_canal(piano))
    changement_canal(piano)
    piano.canal.place(x=5, y=5)
    ## Widget de changement de famille d'instrument
    piano.famille = tk.Spinbox(piano, values=list(inst.INSTRUMENTS), width=20, wrap=True, state='readonly')
    piano.famille.configure(command = lambda: changement_famille(piano))
    piano.famille.place(x=60, y=5)
    ## Widget de changement d'instrument
    piano.instrument = tk.Spinbox(piano, values=list(inst.INSTRUMENTS[piano.famille.get()]), width=20, wrap=True, state='readonly')
    piano.instrument.configure(command = lambda: changement_instrument(piano))
    piano.instrument.place(x=200, y=5)
    changement_instrument(piano)
    ## Widget de changement de volume
    volume_initial = tk.IntVar() # https://stackoverflow.com/questions/32145376/how-can-i-establish-a-default-string-value-on-a-tkinter-spinbox
    piano.volume = tk.Spinbox(piano, from_ = 0, to=100, textvar = volume_initial, width=3, state='readonly')
    volume_initial.set(50)
    piano.volume.configure(command = lambda: changement_volume(piano))
    piano.volume.place(x=350, y=5)
    return piano

def changement_canal(piano):
    piano.clavier.canal = int(piano.canal.get())

def changement_famille(piano):
    piano.instrument.configure(values = list(inst.INSTRUMENTS[piano.famille.get()]))
    changement_instrument(piano)

def changement_instrument(piano):
    instrument = inst.INSTRUMENTS[piano.famille.get()][piano.instrument.get()]
    pyanote.son.message_controle(piano.clavier.midi, [0xC0 + piano.clavier.canal, instrument, 0])

def changement_volume(piano):
    volume = math.floor(int(piano.volume.get()) * ((255 - MINVOLUME) / 100) + MINVOLUME)
    piano.clavier.volume = volume




if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title = "py@note" 
    sortie_midi = pyanote.son.connecter_sortie()
    params_touches = {
        "blanche": {"w" : 30, "h": 100, "couleur": "ivory"},
        "noire": {"w" : 20, "h": 60, "couleur": "black"}
    }
    piano = creer_piano(fenetre, sortie_midi, 3, 5, params_touches)
    piano.pack()
    fenetre.mainloop()