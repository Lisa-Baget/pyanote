import pyanote.resume as res
import pyanote.album as alb
import pyanote.controleur as cont
import pyanote.son as son
import tkinter
from tkinter.filedialog import askopenfilename
import datetime as dt

### en mode analyse le controleur ne fera jamais de time.sleep()
### donc ca va aller tres vite
### et a la fin on aura toutes les infos dispos dans le controleur

def creer_analyse(nom_fichier, sortie_midi):
    resume = res.creer_resume(nom_fichier)
    album = alb.creer_album(resume)
    controleur = cont.creer_controleur(resume, sortie_midi, True)
    cont.jouer_album(album, controleur)
    return controleur

def calculer_duree(analyse):
    return dt.timedelta(0, 0, analyse['temps_micros'])

def calculer_canaux_disponibles(analyse):
    canaux = []
    for i in range(len(analyse['canaux libres'])):
        if analyse['canaux libres'][i]:
            canaux.append(i)
    return canaux

root = tkinter.Tk()
root.withdraw() # https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
nom_fichier = askopenfilename()
midi = son.connecter_sortie()
analyse = creer_analyse(nom_fichier, midi)
print("Durée:", calculer_duree(analyse))
print("Canaux disponibles:", calculer_canaux_disponibles(analyse))