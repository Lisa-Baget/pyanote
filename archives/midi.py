import pygame.midi
import time
import musique


def démarrer():
    pygame.midi.init() #initialise prgm midi
    gadget = pygame.midi.get_default_output_id()#trouve ou est le programme midi sur ordi 
    midi = pygame.midi.Output(gadget)#se sert en sortie sond
#pygame.midisource plus stackoverflow play midi files python?
    return midi


def changer_instrument(midi, instrument, canal):
    midi.set_instrument(instrument, canal)
        #voire liste instruments midi


def jouer_note(midi, note, volume, canal, temps):
    midi.note_on(note, volume, canal) #doc pygame.midi source
    time.sleep(temps)
    midi.note_off(note, volume, canal)

def jouer_notes(midi, notes, volume, canal, temps):
    for note in notes:
        jouer_note(midi, note, volume, canal, temps)


def jouer_notes_temps(midi, partition, volume, canal):
    for paire in partition :
        jouer_note(midi, paire[0], volume, canal, [1])
        
def jouer_accord(midi, accord, volume,canal, temps):
    for note in accord:
        midi.note_on(note, volume, canal)
    time.sleep(temps)
    for note in accord:
        midi.note_off(note, volume, canal)

def jouer_accords(midi, accords, volume, canal, temps):
    for accord in accords:
        jouer_accord(midi, accord, volume, canal, temps)

def jouer_accords_temps(midi, partition, volume, canal):
    for paire in partition:
        jouer_accord( midi, paire[0], volume, canal, paire[1])


def jouer_note_lettre(midi, notes, volume, canal, temps):
    notes_chiffrées = []
    musique.chiffrer_midi_notes(notes)
    for note in notes:
        jouer_note(midi, note, volume, canal, temps)



def eteindre():
    pygame.midi.quit()
