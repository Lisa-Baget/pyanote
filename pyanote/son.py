#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pyanote.son

(C) Lisa Baget, 2018-2019 <li.baget@laposte.net>

Ce module contient les fonctions permettant de jouer un unique message Midi.
"""

import pygame.midi as pgm

pgm.init()
DEFAULT =  pgm.get_default_output_id()

def connecter_sortie(ident=DEFAULT):
    return pgm.Output(ident)

def message(sortie_son, message):
    if len(message) == 3:
        message_controle(sortie_son, message)
    elif len(message) == 1:
        message_systeme(sortie_son, message)
    else:
        raise ValueError("La sortie MIDI ne prend pas en compte les messages meta.")

def message_controle(sortie_son, message):
    sortie_son.write_short(*message)

def message_systeme(sortie_son, message):
    sortie_son.write_sys_ex(0, *message)

def deconnecter(sortie_son):
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
    deconnecter(sortie_son)

