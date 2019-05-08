import pyanote.resume as res
import pyanote.album as alb
import pyanote.son as son
import pyanote.controleur as controle
import tkinter
from tkinter.filedialog import askopenfilename

### Attention ça ne marche pas comme il faut!
### La fonction Lire() prend tout le temps disponible
### Donc l'interface Tkinter est gelée
### Solution: utiliser un thread pour la lecture
### Travail en cours

def Lire():
    nom = askopenfilename()
    resume = res.creer_resume(nom)
    album = alb.creer_album(resume)
    midi = son.connecter_sortie()
    controleur = controle.creer_controleur(resume, midi)
    controle.jouer_album(album, controleur)

fenetre = tkinter.Tk()
fenetre.title("Py@Note")

# creation du menu
menubar = tkinter.Menu(fenetre)

menufichier = tkinter.Menu(menubar,tearoff=0)
menufichier.add_command(label="Ouvrir un fichier", command = Lire)
menufichier.add_command(label="Quitter",command = fenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

fenetre.config(menu=menubar)

fenetre.mainloop()
