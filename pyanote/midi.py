#!/usr/bin/python
# -*- coding: utf-8 -*-
"""pyanote.midi

(C) Phandaal, 2017

Test utilisation des DLLs Window pour envoyer des messages MIDI. Donné au projet pyanote pour
tenter de résoudre des problèmes liés à pygame.
"""

from pyanote.win32midi import Win32Midi

class Midi(Win32Midi):

    def __init__(self):
        Win32Midi.__init__(self)
        self.open_device()

    def short_message(self, code, channel, byte1, byte2):
        message = channel + 0x10 * code + 0x100 * byte1 + 0x10000 * byte2
        Win32Midi.short_message(self, message)

    def short_message_aux(self, status, byte1, byte2):
        message = status + byte1 * 0x100 + byte2 * 0x10000
        Win32Midi.short_message(self, message)

    def note_on(self, note, velocity, channel):             #OK
        self.short_message(0x9, channel, note, velocity)

    def note_off(self, note, velocity, channel):            #OK
        self.short_message(0x8, channel, note, velocity)

    def set_instrument(self, instrument, channel):          #OK
        self.short_message(0xC, channel, instrument, 0)

    def afterTouch(self, note, pressure, channel): ### Ca marche?
        self.short_message(0xA, channel, note, pressure)

    def pitchBend(self, bend, channel):  ### Ca marche ?
        self.short_message(0xD, channel, bend // 2**7, bend % 2**7)


if __name__ == '__main__':
    import time

    midi = Midi()

    midi.short_message(0x9, 0, 60, 200)
    time.sleep(0.5)
    midi.short_message(0x8, 0, 60, 200)

