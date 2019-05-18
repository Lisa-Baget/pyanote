import tkinter as tk
import pyanote.notes
import pyanote.son
import time

def creer_clavier(emplacement, sortie_midi, octave_debut, nb_octaves, params):
    largeur_octave = params['blanche']['w'] * 7
    clavier = tk.Canvas(emplacement, width = nb_octaves * largeur_octave, height = params['blanche']['h'])
    clavier.touches, clavier.midi = {}, sortie_midi
    clavier.canal, clavier.volume, clavier.delai_arret = 0, 200, 250
    note_debut = pyanote.notes.note_vers_nombre("C" + str(octave_debut))
    for i in range(nb_octaves):
        creer_octave(clavier, largeur_octave * i, note_debut + i * 12, params)
    return clavier

def creer_octave(clavier, x_octave, note_debut, params):
    intervalles = [0, 2, 4, 5, 7, 9, 11]
    for i in range(len(intervalles)):
        creer_touche(clavier, note_debut + intervalles[i], x_octave + (i * params['blanche']['w']), params['blanche'])
    for i in range(1, len(intervalles)):
        if intervalles[i] - intervalles[i-1] == 2:
            x = x_octave + (i * params['blanche']['w']) - params['noire']['w'] / 2
            creer_touche(clavier, note_debut + intervalles[i] - 1, x, params['noire'])

def creer_touche(clavier, note, x, param):
    touche = tk.Canvas(clavier, width=param['w'], height=param['h'], bg=param['couleur'])
    clavier.touches[note] = touche
    touche.place(x=x, y=0)
    touche.note = note
    touche.bind("<Button-1>", appuyer_touche)
    touche.bind("<ButtonRelease-1>", relacher_touche)

def appuyer_touche(evenement):
    note = evenement.widget.note
    clavier = evenement.widget.master
    jouer_note(clavier, note)

def jouer_note(clavier, note):
    pyanote.son.message_controle(clavier.midi, [0x90 + clavier.canal, note, clavier.volume])

def relacher_touche(evenement):
    clavier = evenement.widget.master
    note = evenement.widget.note
    evenement.widget.after(250, arreter_note, clavier, note)

def arreter_note(clavier, note):
    pyanote.son.message_controle(clavier.midi, [0x80 + clavier.canal, note, 0])
    
if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title = "py@note" 
    sortie_midi = pyanote.son.connecter_sortie()
    pyanote.son.message_controle(sortie_midi, [0xC0, 0x6D, 0])
    params_touches = {
        "blanche": {"w" : 30, "h": 100, "couleur": "ivory"},
        "noire": {"w" : 20, "h": 60, "couleur": "black"}
    }
    clavier = creer_clavier(fenetre, sortie_midi, 3, 3, params_touches)
    clavier.pack()
    fenetre.mainloop()

