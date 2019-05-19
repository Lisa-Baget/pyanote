#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.mod_midi

(C) Lisa Baget, 2018-2019

Ce module définit un modificateur de controleur permettant de stopper 
les notes quand on met le controleur en pause ou en arret. Sans ce module,
les notes qui n'ont pas reçu de nore off vont continuer à jouer indéfiniment.
"""

def creer_modificateur_vidage_notes():
    ''' Ce modificateur sert à  stopper les notes quand on pause on on arrete le controleur.
    '''
    return {'nom' : 'mod_vidage_notes',
            'init' : {'notes_actives' : initialiser_notes_actives()},
            'prerequis' : [],
            'fonctions' : {
                'mod_message_controle': gerer_notes,
                'mod_pause': vider_notes,
                'mod_arret': vider_notes
                }}

def initialiser_notes_actives():
    notes_actives = []
    for i in range(16): # pour chaque canal
        notes_actives.append(set([]))
    return notes_actives

def gerer_notes(controleur, num_piste, message):
    instruction = message[0] // 16
    canal = message[0] % 16
    if instruction == 9 and canal != 9: # c'est un note on mais pas une batterie
        controleur['notes_actives'][canal].add(codage(num_piste, message[1])) ## on active la note sur le canal
    elif instruction == 8: # c'est un note off
        controleur['notes_actives'][canal].discard(codage(num_piste, message[1])) ## on desactive

def codage(num_piste, note):
    return 128 * note + num_piste

def decodage(code):
    return code % 128, code // 128 

def vider_notes(controleur):
    for canal in range(16):
        for code in controleur['notes_actives'][canal]:
            num_piste, note = decodage(code)
            evenement = [0, num_piste, [0x80 + canal, note, 0]] ## msg note off
            controleur['evenements_urgents'].append(evenement)
        controleur['notes_actives'][canal] = set([]) ## vider l'ensemble

if __name__ == '__main__':
    import pyanote.controleur as cont
    import pyanote.mod_midi as modmid
    import pyanote.son as son
    import time
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    sortie_midi = son.connecter_sortie()
    controleur = cont.creer_controleur(nom_fichier, True)
    modificateur1 = modmid.creer_modificateur_midi(sortie_midi)
    cont.ajouter_modificateur_controle(controleur, modificateur1)
    modificateur2 = creer_modificateur_vidage_notes()
    cont.ajouter_modificateur_controle(controleur, modificateur2)
    print("Demarrage du thread")
    cont.demarrer(controleur)
    time.sleep(15)
    print("Notes actives", controleur['notes_actives'])
    controleur['pause'] = True
    time.sleep(5)
    controleur['pause'] = False
    time.sleep(10)
    print("Notes actives", controleur['notes_actives'])
    controleur['fin'] = True
    controleur['thread'].join()



    son.deconnecter(sortie_midi)