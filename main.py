import serial
import time
import pygame
import pygame.midi

pygame.midi.init()
keyboard = pygame.midi.Input(3, 1000)

rgb = [0, 0, 0]
changed = True
bright = 0.5


with serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=1) as controller:
    time.sleep(3)

    while 1:   
        if(pygame.midi.Input.poll(keyboard)):
            midi_data = pygame.midi.Input.read(keyboard, 1)[0][0]
            if midi_data[0] == 144:
                note = midi_data[1]
                power = midi_data[2]
                print(midi_data)
                if note > 20 and note <= 54:
                    rgb[0] = rgb[0] + power * bright
                    if rgb[0] > 255:
                        rgb[0] = 255
                elif note > 54 and note <= 75:
                    rgb[1] = rgb[1] + power * bright
                    if rgb[1] > 255:
                        rgb[1] = 255
                elif note > 75 and note <= 108:
                    rgb[2] = rgb[2] + power * bright
                    if rgb[2] > 255:
                        rgb[2] = 255
            elif midi_data[0] == 176:
                if midi_data[1] == 1:
                    bright = midi_data[2] / 127

        if rgb[0] >= 1:
            rgb[0] -= 1
            changed = True
        if rgb[1] >= 1:
            rgb[1] -= 1
            changed = True
        if rgb[2] >= 1:
            rgb[2] -= 1
            changed = True
        
        if changed == True:
            colour = int(rgb[2]).to_bytes(1, "big") + int(rgb[0]).to_bytes(1, "big") + int(rgb[1]).to_bytes(1, "big")
            controller.write(colour)
            print(controller.read(3))
            changed = False

        
        time.sleep(0.005)