
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.main

(C) Lisa Baget et Matthieu Durand, 2018-2019

Ce module contient les fonctions permttant de construire la fenêtre pricnipale pyanote.
"""
import tkinter as tk
import pyanote.son as son
import pyanote.piano as pia 
import pyanote.lecteur as lec
import pyanote.karaoke as pkar


def creer_fenetre_pyanote(racine, sortie_midi, params):
    hauteur = 346 + params['piano']['params_touches']['blanche']['h']
    largeur = params['piano']['nb_octaves'] * 7 * params['piano']['params_touches']['blanche']['w']
    racine.configure(width = largeur, height = hauteur)
    racine.title("py@note") 
    piano = pia.creer_piano(racine, sortie_midi, 3, 5, params['piano']['params_touches'])
    piano.place(x=0, y=300)
    karaoke = pkar.creer_karaoke(racine)
    karaoke.place(x=0, y=0)
    lecteur = lec.creer_lecteur(racine, sortie_midi, piano, karaoke)
    lecteur.place(x = largeur - 300, y=0)

if __name__ == "__main__":
    sortie_midi = son.connecter_sortie()
    params = {
        "piano" : {
            "octave_debut": 3,
            "nb_octaves": 4,
            "params_touches" : {
                "blanche": {"w" : 40, "h": 180, "couleur": "ivory", "altcouleur": "ghostwhite", "text": "lightgray"},
                "noire": {"w" : 24, "h": 110, "couleur": "black", "altcouleur": "gray", "text": "silver"}
            }
        },
        "widgets" : {

        }
    }
    racine = tk.Tk()
    creer_fenetre_pyanote(racine, sortie_midi, params)
    barre_menu = tk.Menu(racine)
    menufichier = tk.Menu(barre_menu,tearoff=0)
    menufichier.add_command(label="Ouvrir", command = lambda: print(1))
    menufichier.add_command(label="Quitter",command = racine.destroy)
    barre_menu.add_cascade(label="Fichier", menu=menufichier)
    racine.config(menu=barre_menu)
    racine.mainloop()

