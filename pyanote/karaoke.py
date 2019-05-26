"""pyanote.karaoke

(C) Matthieu Durand, 2018-2019

Ce module contient les fonctions permettant de visualiser une interface de karaoke.

Probleme: https://stackoverflow.com/questions/10288554/finding-the-current-size-of-a-tkinter-text-widget
"""
import tkinter as tk

H_LINE = 12
W_CHAR = 7

def creer_karaoke(contenant):
    frame = tk.Canvas(contenant, width = 500, height = 298, bg = 'black')
    karaoke = tk.Canvas(frame, width = 480, height = 283, bg = 'darkslategrey')
    frame.texte = karaoke
    frame.identifiants = {}
    frame.sauvegarde = False
    ## Tout ça c'est la gstion du scrollbar, copié sur intrenet, rien compris
    karaoke.configure(scrollregion = karaoke.bbox("all"))
    karaoke.pack(side = 'left', fill = 'both')
    defilY = tk.Scrollbar(frame, orient = 'vertical')
    defilY.pack(side = 'right', fill = 'y')
    frame.scroll = defilY
    karaoke.configure(yscrollcommand = defilY.set)
    defilY.config(command = karaoke.yview)
    return frame



def mettre_a_jour_karaoke(karaoke, paroles):
    ## on commence a effacer ce qui peut rester d'une autre chanson
    for temps in karaoke.identifiants:
        karaoke.texte.delete(karaoke.identifiants[temps]) 
    ## et on construit le prochain
    coords = [0, 0]
    for ticks, texte in paroles.items():
        if ticks == 0:
            ident = creer_titre(karaoke, texte, coords)
        else:
            ident = creer_syllabe(karaoke, ticks, texte, coords)
        karaoke.identifiants[ticks] = ident
    karaoke.texte.configure(scrollregion = karaoke.texte.bbox("all"))
    

def creer_titre(karaoke, liste_texte, coords):
    police = ("Digital-7 Mono", 12, 'bold')
    titre = ''
    for texte in liste_texte:
        if texte[0:2] == '@T':
            titre = titre + texte[2:] + '\n'
            coords[1] = coords[1] + 1.5 * H_LINE
    return karaoke.texte.create_text((10, 0), text = titre, font = police, anchor = 'nw', fill = "darkgreen")

def creer_syllabe(karaoke, ticks, texte, coords):
    police = ('Digital-7 Mono', 10, 'bold')
    #print(texte)
    if len(texte) != 0:
        if texte[0] == '\\': # attention escape char, '\\' veut juste dire '\'
            coords[1] = coords[1] + 2.5 * H_LINE
            coords[0] = 10
            ident = karaoke.texte.create_text(coords, text = texte[1:], font = police, anchor = 'nw', fill = "green")
            coords[0] = coords[0] + (len(texte) - 1) * W_CHAR
            return ident
        elif texte[0] == '/':
            coords[1] = coords[1] + H_LINE
            coords[0] = 10
            ident = karaoke.texte.create_text(coords, text = texte[1:], font = police, anchor = 'nw', fill = "green")
            coords[0] = coords[0] + (len(texte) - 1) * W_CHAR
            return ident
        else:
            ident = karaoke.texte.create_text(coords, text = texte, font = police, anchor = 'nw', fill = "green")
            coords[0] = coords[0] + len(texte) * W_CHAR
    return ident



def changer_couleur_karaoke(karaoke, ticks):
    if karaoke.sauvegarde:
        karaoke.texte.itemconfig(karaoke.sauvegarde, fill = 'green')
    karaoke.texte.itemconfig(karaoke.identifiants[ticks], fill = 'lime')
    karaoke.sauvegarde = karaoke.identifiants[ticks]



