import tkinter as tk
from tkinter.filedialog import askopenfilename
import pyanote.resume as res
import sys
#import pyanote.son as son
import pyanote.controleur as cont
import pyanote.mod_temps_total as modtt
import pyanote.mod_midi as modmd
import pyanote.mod_vidage_notes as modvn
import pyanote.mod_comptage_temps as modct
import time


def creer_lecteur(maitre, midi):
    # initialisation du lecteur
    lecteur = tk.Frame(maitre, width = 300, height = 300)
    maitre.lecteur = lecteur
    lecteur.actif = False ### on n'a pas chargé de fichier
    lecteur.pause = True ### on est en pause
    lecteur.midi = midi
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
    label = tk.Label(lecteur, text="Lecteur MIDI py@note", font=police)
    label.place(x=0, y=0, height=20, width=300)
    return label

def creer_affichage_fichier(lecteur):
    police = ('Digital-7', 10, 'normal')
    label = tk.Label(lecteur, text="Cliquez ici pour ouvrir un fichier", font=police, relief="sunken", background="silver", foreground='whitesmoke')
    label.bind("<Button-1>", changer_fichier)
    label.place(x=0, y=20, height=20, width=300)
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
    mod1 = modtt.creer_modificateur_temps()
    cont.ajouter_modificateur_controle(lecteur.controleur, mod1)
    lecteur.controleur['vitesse'] = float('inf')
    cont.demarrer(lecteur.controleur)
    lecteur.defilement.configure(to = lecteur.controleur['temps/chanson'][0] // 10**6)
    cont.initialiser_valeurs_defaut(lecteur.controleur)
    ## FIN ANALYSE
    lecteur.controleur['thread'] = True
    mod2 = modmd.creer_modificateur_midi(lecteur.midi)
    cont.ajouter_modificateur_controle(lecteur.controleur, mod2)
    mod3 = modvn.creer_modificateur_vidage_notes()
    cont.ajouter_modificateur_controle(lecteur.controleur, mod3)
    mod4 = modct.creer_modificateur_comptage(lecteur.horloge, lecteur.defilement)
    cont.ajouter_modificateur_controle(lecteur.controleur, mod4)
    lecteur.actif = True
    nom_court = nouveau_fichier.split('/')[-1]
    lecteur.fichier.configure(text=nom_court)
    for nom_bouton in lecteur.boutons:
        lecteur.boutons[nom_bouton].configure(state = 'normal')
    demarrer_lecture(lecteur)

def creer_affichage_pistes(lecteur):
    frame = tk.Frame(lecteur, height=200, width=300)
    frame.place(x=0, y=40)
    return frame

def creer_afficheur_temps(maitre):
    #police = ('courier', 12, 'bold')
    police = ('Digital-7 Mono', 12, 'bold')
    afficheur = tk.Label(maitre, text="00:00", relief="sunken", font=police, padx=3, pady=3, background="silver", foreground='whitesmoke')
    afficheur.place(x = 10, y = 235)
    return afficheur


def creer_defilement_temps(maitre, debut, fin):
    #frame = tk.Frame(maitre, width=300, height=40)
    barre = tk.Scale(maitre, from_=debut, to=fin, orient="horizontal", width = 15, length = 210, showvalue=False)
    barre.configure(command=lambda val: changer_barre_temps(maitre, val))
    barre.place(x=80, y = 235)
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
    bouton = tk.Button(maitre, image=photo, command=nom_fonction, background="lightgrey")
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
    cont.demarrer(bouton.master.controleur)

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
    time.sleep(0.1)
    son.deconnecter(midi)
    fenetre.destroy()

def maj_temps(fenetre, temps):
    fenetre.lecteur.horloge.configure(text = str(temps)) 

if __name__ == "__main__":
    import time
    fenetre = tk.Tk()
    import pyanote.son as son
    fenetre.title("py@Note")
    midi = son.connecter_sortie()
    lecteur = creer_lecteur(fenetre, midi)
    lecteur.pack()
    fenetre.wm_protocol('WM_DELETE_WINDOW', lambda: quitter(fenetre, midi, lecteur))
    fenetre.mainloop()