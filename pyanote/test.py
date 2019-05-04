import lecturemidi
import lecturesons
import time


def jouer(midi, temps, message):
    attendre(temps)
    if message[0]== 'systeme':
        print('systeme')
    elif message[0] == 'meta':
        print('meta')
    else:
        jouer_message(midi, message)


def jouer_message(midi, message):
    status = message[1]*16 + message[2] #? addition?
    midi.write_short(status, message[3], message[4])
    print([status,message[3],message[4]])
        
def attendre(temps):
    time.sleep(temps/1000)


if __name__ == "__main__":
    nom ="../exemples/Dave Brubeck - Take Five 1.mid"
    descrip = lecturemidi.preparer_midi(nom)
    midi = lecturesons.demarrer()
#    midi.write_short(0x90, 60, 120)
    for element in lecturemidi.enumerer_pistes(descrip):
        jouer(midi, element[0], element[1])
