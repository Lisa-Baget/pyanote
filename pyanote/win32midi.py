#!/usr/bin/python
# -*- coding: utf-8 -*-
"""pyanote.win32midi

(C) Phandaal, 2017

Ce module contient les fonctions permettant de lire des informations simples dans un fichier binaire Midi.

DONE
"""
from sys import platform
from ctypes import windll
from ctypes import byref, sizeof, string_at, cast
from ctypes import Structure, c_void_p, c_int, c_char_p, wintypes

class Win32Midi():

    def __init__(self):
        assert platform == 'win32'
        self.dll = windll.winmm

    def get_number_devices(self):
        """ Returns the number of MIDI devices available on the Windows platform.
        """
        return self.dll.midiOutGetNumDevs()

    def get_device_info(self, device_id=-1): # Pour l'instant il n'y a que le nom qui marche
        struct = _MIDIOUTCAPS()
        res = self.dll.midiOutGetDevCapsA(device_id, byref(struct), sizeof(struct))
        name = string_at(cast(struct.szPname, c_char_p))
        return name.decode(encoding="utf-8")

    def open_device(self, device_id=-1):
        self.midi = c_void_p()
        err_code = self.dll.midiOutOpen(byref(self.midi), device_id, 0, 0, 0)
        if err_code != 0:
            raise Win32MidiException(err_code)
        else:
            self.id = device_id

    def close_device(self):
        res = self.dll.midiOutClose(self.midi)
        return res

    def short_message(self, midi_message : int):
        err_code = self.dll.midiOutShortMsg(self.midi, c_int(midi_message))
        if err_code != 0:
            raise Win32MidiException(err_code)




class Win32MidiException(Exception):

    MIDI_ERR_BASE = 64
    MIDIERR_NODEVICE = MIDI_ERR_BASE + 4
    MIDIERR_BADOPENMODE = MIDI_ERR_BASE + 6
    MIDIERR_NOTREADY = MIDI_ERR_BASE + 3
    MMSYSERR_BASE = 0
    MMSYSERR_ALLOCATED = MMSYSERR_BASE + 4
    MMSYSERR_BADDEVICEID = MMSYSERR_BASE + 2
    MMSYSERR_INVALPARAM = MMSYSERR_BASE + 11
    MMSYSERR_NOMEM = MMSYSERR_BASE + 7
    MMSYSERR_INVALHANDLE = MMSYSERR_BASE + 5

    ERR_CODES = {
        MIDIERR_NODEVICE :
            "No MIDI port was found.",
        MMSYSERR_ALLOCATED :
            "The specified resource is already allocated.",
        MMSYSERR_BADDEVICEID :
            "The specified device identifier is out of range.",
        MMSYSERR_INVALPARAM :
            "The specified pointer or structure is invalid.",
        MMSYSERR_NOMEM :
            "The system is unable to allocate or lock memory.",

        MIDIERR_BADOPENMODE :
            "The application sent a message without a status byte to a stream handle.",
        MIDIERR_NOTREADY :
            "The hardware is busy with other data.",
        MMSYSERR_INVALHANDLE :
            "The specified device handle is invalid."
    }

    UNKNOWN = "Unknown Exception with return value "


    def __init__(self, err_code):
        msg = self.ERR_CODES.get(err_code, self.UNKNOWN + str(err_code))
        Exception.__init__(self, msg)


class _MIDIOUTCAPS(Structure):

    _fields_ = [

        ('wMid', wintypes.WORD),
        ('wPid', wintypes.WORD),
        ('vDriverVersion', wintypes.UINT),
        ('szPname', wintypes.BYTE * 64),
        ('wTechnology', wintypes.WORD),
        ('wVoices', wintypes.WORD),
        ('wNotes', wintypes.WORD),
        ('wChannel_mask', wintypes.WORD),
        ('dwSupport', wintypes.DWORD),
    ]


