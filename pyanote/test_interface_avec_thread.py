import pyanote.thread as pt
import tkinter
from tkinter.filedialog import askopenfilename

### Maintenant, avec le thread, l'interface n'est plus gelee
### probleme 1: quand on pause entre un note_on et un note_off,
### la note continue a jouer indefiniment
### Solution: garder dans le controleur la liste de toutes les
### notes en train d'être jouées
### probleme 2: quand on ouvre un fichier sur un fichier deja ouvert, 
### ça met le bazar. pourquoi???

controleur = {}

def Ouvrir():
    nom_fichier = askopenfilename()
    global controleur
    controleur = pt.preparer_lecture(nom_fichier)
    pt.demarrer_lecture(controleur)

def Pause():
    global controleur
    if controleur["pause"]:
        pt.reprendre_lecture(controleur)
    else:
        pt.pause_lecture(controleur)

def Stopper():
    global controleur
    pt.arreter_lecture(controleur)
    
fenetre = tkinter.Tk()
fenetre.title("Py@Note")


# creation du menu
menubar = tkinter.Menu(fenetre)

menufichier = tkinter.Menu(menubar,tearoff=0)
menufichier.add_command(label="Ouvrir", command = Ouvrir)
menufichier.add_command(label="Pause", command = Pause)
menufichier.add_command(label="Stopper", command = Stopper)
menufichier.add_command(label="Quitter", command = fenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

fenetre.config(menu=menubar)

fenetre.mainloop()
