import pygame.midi as pgm
import time
pgm.init()
identificateur = pgm.get_default_output_id()
sortie_son = pgm.Output(identificateur)
print(identificateur)
print(sortie_son)
sortie_son.write_short(0xC0, 27, 0)
sortie_son.write_short(0x90, 60, 240)
time.sleep(2)
sortie_son.write_short(0x80, 60, 240)
sortie_son.close()