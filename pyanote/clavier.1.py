import tkinter as tk
import pyanote.notes
import pyanote.son
import time

def creer_clavier(emplacement, sortie_midi, octave_debut, nb_octaves, params):
    largeur_octave = params['blanche']['w'] * 7
    clavier = tk.Canvas(emplacement, width = nb_octaves * largeur_octave, height = params['blanche']['h'])
    clavier.touches, clavier.octaves, clavier.midi = {}, [], sortie_midi
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
    touches_ordi = ['q', 'z', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h']
    octave.notes = {}
    for i in range(len(touches_ordi)):
        octave.notes[touches_ordi[i]] = note_debut + i
        appuie = '<KeyPress-' + touches_ordi[i] + '>'
        relache = '<KeyRelease-' + touches_ordi[i] + '>'
        octave.bind(appuie, appuyer_touche_clavier)
        octave.bind(relache, relacher_touche_clavier)


def creer_touche(octave, note, x, param):
    touche = tk.Canvas(octave, width=param['w'], height=param['h'], bg=param['couleur'])
    octave.master.touches[note] = touche
    touche.place(x=x, y=0)
    touche.note = note
    touche.appuyee = False
    touche.bind("<Button-1>", appuyer_touche_souris)
    touche.bind("<ButtonRelease-1>", relacher_touche_souris)

def appuyer_touche_souris(evenement):
    appuyer_touche(evenement.widget.master.master, evenement.widget.note)

def appuyer_touche_clavier(evenement):
    ### probleme ici, l'evenement est lancé plein de fois pendant que la touche est appuyée
    ### ca a l'air normal: https://stackoverflow.com/questions/33088597/python-tkinter-keypress-event-trigger-once-hold-vs-pressed
    ### on adapte la solution
    clavier = evenement.widget.master
    note = evenement.widget.notes[evenement.char]
    touche = clavier.touches[note]
    if not touche.appuyee:
        appuyer_touche(clavier, note)

def appuyer_touche(clavier, note):
    touche = clavier.touches[note]
    touche.appuyee = True
    jouer_note(clavier, note)

def jouer_note(clavier, note):
    pyanote.son.message_controle(clavier.midi, [0x90 + clavier.canal, note, clavier.volume])

def relacher_touche_souris(evenement):
    relacher_touche(evenement.widget.master.master, evenement.widget.note)

def relacher_touche_clavier(evenement):
    relacher_touche(evenement.widget.master, evenement.widget.notes[evenement.char])

def relacher_touche(clavier, note):
    touche = clavier.touches[note]
    touche.appuyee = False
    clavier.after(250, arreter_note, clavier, note)

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

