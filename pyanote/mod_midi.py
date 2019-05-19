#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.mod_midi

(C) Lisa Baget, 2018-2019

Ce module définit un modificateur de controleur permettant de jouer les
notes dans une sortie Midi.
"""
import pyanote.son as son

def creer_modificateur_midi(sortie_midi):
    ''' Ce modificateur sert à  lier les messages controle et les messages systeme à une sortie MIDI.
    '''
    return {'nom' : 'mod_midi',
            'init' : {'midi' : sortie_midi},
            'prerequis' : [],
            'fonctions' : {
                'mod_message_controle': lire_message_controle,
                'mod_message_systeme': lire_message_systeme}}

def lire_message_controle(controleur, num_piste, message):
    son.message_controle(controleur['midi'], message)

def lire_message_systeme(controleur, num_piste, message):
    son.message_systeme(controleur['midi'], message)

if __name__ == '__main__':
    import pyanote.controleur as cont
    nom_fichier = 'fichiersMidi/Dave Brubeck - Take Five.mid'
    sortie_midi = son.connecter_sortie()
    controleur = cont.creer_controleur(nom_fichier)
    modificateur = creer_modificateur_midi(sortie_midi)
    cont.ajouter_modificateur_controle(controleur, modificateur)
    cont.demarrer(controleur)
    son.deconnecter(sortie_midi)