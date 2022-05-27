import time
import pygame
import pygame.midi

pygame.midi.init()
keyboard = pygame.midi.Input(3, 1000)



while 1:   
    if(pygame.midi.Input.poll(keyboard)):
        midi_data = pygame.midi.Input.read(keyboard, 1)
        print(midi_data)

    time.sleep(0.01)