import pyanote.thread as pt
import pyanote.son as son
import tkinter
from tkinter.filedialog import askopenfilename

### Maintenant, avec le thread, l'interface n'est plus gelee
### probleme 1: quand on pause entre un note_on et un note_off,
### la note continue a jouer indefiniment
### Solution: garder dans le controleur la liste de toutes les
### notes en train d'être jouées
### probleme 2: quand on ouvre un fichier sur un fichier deja ouvert, 
### ça met le bazar. pourquoi???

parametres = [{}, son.connecter_sortie()]

def Ouvrir():
    nom_fichier = askopenfilename()
    global parametres
    parametres[0] = pt.preparer_lecture(nom_fichier, parametres[1]) # recuperation du controleur
    #inserer_dictionnaire(controleur, pt.preparer_lecture(nom_fichier)) # probleme ici
    pt.demarrer_lecture(parametres[0])

def Pause():
    global parametres
    if parametres[0]["pause"]:
        pt.reprendre_lecture(parametres[0])
    else:
        pt.pause_lecture(parametres[0])

def Stopper():
    global parametres
    pt.arreter_lecture(parametres[0])

def Imprimer():
    global parametres
    print(parametres[0])

def inserer_dictionnaire(dic1, dic2):
    for cle in dic2:
        dic1[cle] = dic2[cle]
    
fenetre = tkinter.Tk()
fenetre.title("Py@Note")


# creation du menu
menubar = tkinter.Menu(fenetre)

menufichier = tkinter.Menu(menubar,tearoff=0)
menufichier.add_command(label="Ouvrir", command = Ouvrir)
menufichier.add_command(label = "Test", command = Imprimer)
menufichier.add_command(label="Pause", command = Pause)
menufichier.add_command(label="Stopper", command = Stopper)
menufichier.add_command(label="Quitter", command = fenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

fenetre.config(menu=menubar)

fenetre.mainloop()
