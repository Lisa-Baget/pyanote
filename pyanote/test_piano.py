import tkinter as tk
import pyanote.son as son

def creer_piano(maitre, midi, canal, octave_debut, nb_octaves, w_touche=20, h_touche=100, couleurs=["ivory", "ghostwhite", "black", "gray"]):
    canvas = tk.Canvas(maitre, width = 7 * nb_octaves * w_touche, height = h_touche)
    canvas.touches = {}
    canvas.midi = midi
    canvas.canal = canal
    for i in range(nb_octaves):
            creer_octave(canvas, 12 * (i + octave_debut + 1), i * w_touche * 7, w_touche, h_touche, couleurs)
    return canvas

def creer_octave(canvas, note_debut, w_base, w_touche, h_touche, couleurs):
    notes = [0, 2, 4, 5, 7, 9, 11]
    for i in range(len(notes)): # dessin des blanches
        note = note_debut + notes[i]
        canvas.touches[note] = creer_touche(canvas, w_base + i*w_touche, w_touche, h_touche, couleurs[0], couleurs[1], note)
    for i in range(len(notes) - 1): # dessin des noires
        if (notes[i+1] - notes[i]) == 2: # il y a bien un diese ici
            note = note_debut + 1 + notes[i]
            canvas.touches[note] = creer_touche(canvas, w_base + i*w_touche + 0.65*w_touche, 0.7*w_touche, 0.6*h_touche, couleurs[2], couleurs[3], note)

def creer_touche(canvas, w_base, w_touche, h_touche, couleur1, couleur2, note):
    touche = tk.Canvas(canvas, width=w_touche, height=h_touche, background=couleur1)
    touche.note, touche.couleur1, touche.couleur2 = note, couleur1, couleur2
    touche.parent = canvas
    touche.place(x=w_base, y=0)
    touche.bind("<Button-1>", touche_appuyer)
    return touche

def touche_appuyer(evenement):
    touche = evenement.widget
    message = [9 * 16 + touche.parent.canal, touche.note, 255]
    son.message_controle(touche.parent.midi, message)
    touche.configure(bg = touche.couleur2)
    evenement.widget.after(500, lambda: touche_relacher(touche))

def touche_relacher(touche):
    message = [8 * 16 + touche.parent.canal, touche.note, 255]
    son.message_controle(touche.parent.midi, message)
    touche.configure(bg = touche.couleur1)






if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("py@Note")
    midi = son.connecter_sortie()
    canal = 8
    piano = creer_piano(fenetre, midi, canal, 3, 6, 40, 180)
    piano.pack()

    fenetre.mainloop()