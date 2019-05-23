#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.son

(C) Lisa Baget, 2018-2019

Ce module contient les fonctions permettant de jouer un unique message Midi.
"""
import pygame.midi as pgm


def connecter_sortie():
    ''' Appeler cette fonction pour récupérer une sortie MIDI.
    '''
    pgm.init() ### mettre le init ici va peut etre réler le bug sur le portable
    ident=pgm.get_default_output_id()
    return pgm.Output(ident)

def message_controle(sortie_son, message):
    ''' Envoie un message de controle [statut, arg1, arg2] à la sortie son.
    '''
    ### message est une liste de 3 arguments, mais write_short veut 3 args
    ### et pas une liste. On met * pour que ça marche.
    sortie_son.write_short(*message)

def message_systeme(sortie_son, message):
    ''' Envoie un message systeme [chaine_binaire] à la sortie son.
    '''
    sortie_son.write_sys_ex(0, *message)

def deconnecter(sortie_son):
    ''' Ferme la sortie son. Pygame.midi fait un message d'erreur si ce n'est pas
    fermé avant la fin du programme.
    '''
    sortie_son.close()

if __name__ == "__main__":
    import time
    sortie_son = connecter_sortie() 
    message_controle(sortie_son, [0xC0, 27, 0])  # change instrument sur canal 0 (0xC0), jazz guitar (27)
    message_controle(sortie_son, [0x90, 60, 120]) # note on canal 0 (0x90), note 60, velocité 120
    message_controle(sortie_son, [0x90, 65, 120])
    time.sleep(0.5)
    message_controle(sortie_son, [0x80, 60, 120]) # note off: doit le faire pour chaque note on
    message_controle(sortie_son, [0x80, 65, 120])
    message_controle(sortie_son, [0xC0, 66, 0]) # alto sax
    message_controle(sortie_son, [0x90, 60, 120])
    message_controle(sortie_son, [0x90, 65, 120])
    time.sleep(1)
    message_controle(sortie_son, [0x80, 60, 120])
    message_controle(sortie_son, [0x80, 65, 120])
    # test pour savoir si on peut faire des note off qui servent a rien: reponse OUI
    message_controle(sortie_son, [0x80, 72, 120]) # note off sur une note non jouée: pas de probleme et c'est tant mieux
    time.sleep(1)
    # test pour savoir quel est le canal batterie
    message_controle(sortie_son, [0x99, 60, 120]) # le 10eme canal, c'est à dire le 9!!!
    time.sleep(1)
    # test pour savoir si un note off peut arreter plusieurs note on: reponse OUI
    message_controle(sortie_son, [0xC0, 57, 0]) # trompette (son long si pas stoppé)
    message_controle(sortie_son, [0x90, 60, 120])
    time.sleep(0.1)
    message_controle(sortie_son, [0xC0, 58, 0]) # autre trompette
    message_controle(sortie_son, [0x90, 60, 120]) # meme note
    time.sleep(2)
    message_controle(sortie_son, [0x80, 60, 120]) # on arrete la note
    time.sleep(3)
    deconnecter(sortie_son)

