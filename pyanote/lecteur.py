#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.lecture

(C) Lisa Baget, 2018-2019

Interface graphique pour lecture de fichiers Midi.

TO DO: acceleration, utilisation de la barre de defilement, retour arriere
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
import sys
import pyanote.controleur as cont
import pyanote.modificateurs as mods

def creer_lecteur(maitre, midi, piano = False, kar = False):
    # initialisation du lecteur
    lecteur = tk.Frame(maitre, width = 300, height = 300, bg = 'black')
    maitre.lecteur = lecteur
    lecteur.kar = kar
    lecteur.actif = False ### on n'a pas chargé de fichier
    lecteur.pause = True ### on est en pause
    lecteur.clavier = piano.clavier
    lecteur.midi = midi
    lecteur.controleur = False
    lecteur.temps = tk.StringVar(lecteur, "00.00")   ### STRINGVAR
    # mise en place des widgets
    lecteur.titre = creer_titre(lecteur)
    lecteur.fichier = creer_affichage_fichier(lecteur)
    lecteur.pistes = creer_affichage_pistes(lecteur)
    lecteur.horloge = creer_afficheur_temps(lecteur)
    lecteur.defilement = creer_defilement_temps(lecteur, 0, 100)
    lecteur.boutons = creer_barre_boutons(lecteur)
    return lecteur

def creer_titre(lecteur):
    police = ('courier', 12, 'bold')
    label = tk.Label(lecteur, text="Lecteur MIDI py@note", font=police, fg='silver', bg = 'black')
    label.place(x=0, y=0, height=20, width=300)
    return label

def creer_affichage_fichier(lecteur):
    police = ('Digital-7', 11, 'bold')
    label = tk.Label(lecteur, text="Cliquez ici pour ouvrir un fichier", font=police, relief="sunken", background="darkslategrey", foreground='lime')
    label.bind("<Button-1>", changer_fichier)
    label.place(x=0, y=20, height=30, width=300)
    return label

def changer_fichier(evenement):
    lecteur = evenement.widget.master
    nouveau_fichier = askopenfilename()
    if lecteur.actif:
        presser_bouton_arret(lecteur)
    try:
        lecteur.controleur = cont.creer_controleur(nouveau_fichier)
    except:
        msg_erreur = sys.exc_info()[1]
        lecteur.fichier.configure(text=msg_erreur)
        return
    ## DEBUT ANALYSE
    lecteur.controleur['vitesse'] = float('inf')
    mods.preparer_modificateurs(lecteur.controleur,  kar = lecteur.kar)
    cont.demarrer(lecteur.controleur)
    lecteur.defilement.configure(to = lecteur.controleur['mod_temps/chanson'][0] // 10**6)
    cont.reinitialiser_controleur(lecteur.controleur)
    ## FIN ANALYSE
    mods.preparer_modificateurs(lecteur.controleur, midi = lecteur.midi, horloge = lecteur.temps, 
        defilement = lecteur.defilement, clavier = lecteur.clavier, kar = lecteur.kar)
    lecteur.controleur['thread'] = True
    lecteur.actif = True
    nom_court = nouveau_fichier.split('/')[-1]
    lecteur.fichier.configure(text=nom_court)
    for nom_bouton in lecteur.boutons:
        lecteur.boutons[nom_bouton].configure(state = 'normal')
    ## Tant qu'on n'a pas géré ces boutons...
    for nom_bouton in ['debut', 'fin', 'arriere', 'avant']:
        lecteur.boutons[nom_bouton].configure(state = 'disabled')
    demarrer_lecture(lecteur)

def creer_affichage_pistes(lecteur):
    frame = tk.Frame(lecteur, height=175, width=280, bg = "darkslategrey", relief = 'sunken')
    frame.place(x = 10, y=55)
    return frame

def creer_afficheur_temps(maitre):
    police = ('Digital-7 Mono', 12, 'bold')
    afficheur = tk.Label(maitre, textvariable=maitre.temps, relief="sunken", font=police, padx=3, pady=3, background="darkslategrey", foreground='lime')
    afficheur.place(x = 10, y = 235)
    return afficheur


def creer_defilement_temps(maitre, debut, fin):
    barre = tk.Scale(maitre, from_=debut, to=fin, orient="horizontal", width = 15, length = 205, showvalue=False)
    barre.configure(command=lambda val: changer_barre_temps(maitre, val))
    barre.configure(bg = 'black', highlightbackground = 'black', troughcolor = 'darkslategrey')
    barre.place(x=80, y = 237)
    return barre

def changer_barre_temps(lecteur, valeur):
    pass

def creer_barre_boutons(lecteur):
    boutons = {}
    boutons["lecture"] = creer_bouton_lecture(lecteur, 35, 265)
    boutons["arret"] = creer_bouton_arret(lecteur, 75, 265)
    boutons["debut"] = creer_bouton_debut(lecteur, 115, 265)
    boutons["fin"] = creer_bouton_fin(lecteur, 155, 265)
    boutons["arriere"] = creer_bouton_arriere(lecteur, 195, 265)
    boutons["avant"] = creer_bouton_avant(lecteur, 235, 265)
    return boutons


def creer_bouton_image(maitre, x, y, nom_fichier, nom_fonction):
    photo = tk.PhotoImage(file=nom_fichier)
    bouton = tk.Button(maitre, image=photo, command=nom_fonction, background= 'silver')
    bouton.image = photo
    bouton.configure(state = 'disabled')
    bouton.place(x=x, y=y)
    return bouton

def creer_bouton_lecture(maitre, ligne, colonne):
    bouton = creer_bouton_image(maitre, ligne, colonne, "pyanote/icones/icons8-jouer-24.png", lambda: presser_bouton_lecture(maitre))
    bouton.configure(state="disabled")
    bouton.pause = True
    bouton.image2 = tk.PhotoImage(file="pyanote/icones/icons8-pause-24.png")
    return bouton

def demarrer_lecture(lecteur):
    bouton = lecteur.boutons['lecture']
    bouton.configure(image=bouton.image2)
    lecteur.pause = False
    cont.demarrer(bouton.master.controleur, True)

def presser_bouton_lecture(lecteur):
    bouton = lecteur.boutons['lecture']
    if lecteur.pause: ### il faut se mettre en lecture
        bouton.configure(image=bouton.image2)
        lecteur.pause = False
        bouton.master.controleur['pause'] = False
    else: ## il faut se mettre en pause
        bouton.configure(image=bouton.image)
        lecteur.pause = True
        bouton.master.controleur['pause'] = True

def creer_bouton_arret(maitre, ligne, colonne):
    bouton = creer_bouton_image(maitre, ligne, colonne, "pyanote/icones/icons8-arrêter-24.png", lambda: presser_bouton_arret(maitre))
    return bouton

def presser_bouton_arret(lecteur):
    for nom_bouton in lecteur.boutons:
        lecteur.boutons[nom_bouton].configure(state = 'disabled')
    if lecteur.controleur:
        lecteur.controleur['fin'] = True
    lecteur.fichier.configure(text="Cliquez ici pour ouvrir un fichier")
    lecteur.actif = False ### on n'a pas chargé de fichier
    lecteur.pause = True ### on est en pause

def creer_bouton_debut(maitre, ligne, colonne):
    bouton = creer_bouton_image(maitre, ligne, colonne, "pyanote\icones\icons8-aller-au-début-24.png", lambda: presser_bouton_debut(maitre))
    return bouton

def presser_bouton_debut(lecteur):
    print("debut")

def creer_bouton_fin(maitre, ligne, colonne):
    bouton = creer_bouton_image(maitre, ligne, colonne, "pyanote\icones\icons8-fin-24.png", lambda: presser_bouton_fin(maitre))
    return bouton

def presser_bouton_fin(lecteur):
    print("fin")

def creer_bouton_arriere(maitre, ligne, colonne):
    bouton = creer_bouton_image(maitre, ligne, colonne, "pyanote/icones/icons8-rembobiner-24.png", lambda: presser_bouton_arriere(maitre))
    bouton.configure(repeatdelay = 200, repeatinterval = 200)
    return bouton

def presser_bouton_arriere(lecteur):
    print("arriere")

def creer_bouton_avant(maitre, ligne, colonne):
    bouton = creer_bouton_image(maitre, ligne, colonne, "pyanote/icones/icons8-avance-rapide-24.png", lambda: presser_bouton_avant(maitre))
    bouton.configure(repeatdelay = 200, repeatinterval = 200)
    return bouton

def presser_bouton_avant(lecteur):
    print("avant")

def charger_fichier(lecteur):
    for nom_bouton in lecteur.boutons:
        lecteur.boutons[nom_bouton].configure(state = 'normal')

def quitter(fenetre, midi, lecteur):
    presser_bouton_arret(lecteur)
    #fenetre.lecteur.controleur['thread'].join()
    ##son.deconnecter(midi)
    fenetre.destroy()

def maj_temps(fenetre, temps):
    fenetre.lecteur.horloge.configure(text = str(temps)) 

if __name__ == "__main__":
    fenetre = tk.Tk()
    import pyanote.son as son
    fenetre.title("py@Note")
    midi = son.connecter_sortie()
    lecteur = creer_lecteur(fenetre, midi)
    lecteur.pack()
    fenetre.wm_protocol('WM_DELETE_WINDOW', lambda: quitter(fenetre, midi, lecteur))
    fenetre.mainloop()