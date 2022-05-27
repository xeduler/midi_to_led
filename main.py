import serial
import time
import pygame
import pygame.midi

pygame.midi.init()
keyboard = pygame.midi.Input(3, 1000)

rgb = [0, 0, 0]
changed = True



with serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=1) as controller:
    time.sleep(3)

    while 1:   
        if(pygame.midi.Input.poll(keyboard)):
            midi_data = pygame.midi.Input.read(keyboard, 1)[0][0]
            note = midi_data[1]
            power = midi_data[2]
            print(midi_data)
            if note > 20 and note <= 50:
                rgb[0] = rgb[0] + power
                if rgb[0] > 255:
                    rgb[0] = 255
            elif note > 50 and note <= 79:
                rgb[1] = rgb[1] + power
                if rgb[1] > 255:
                    rgb[1] = 255
            elif note > 79 and note <= 108:
                rgb[2] = rgb[2] + power
                if rgb[2] > 255:
                    rgb[2] = 255

        if rgb[0] > 0:
            rgb[0] -= 1
            changed = True
        if rgb[1] > 0:
            rgb[1] -= 1
            changed = True
        if rgb[2] > 0:
            rgb[2] -= 1
            changed = True
        
        if changed == True:
            colour = rgb[2].to_bytes(1, "big") + rgb[0].to_bytes(1, "big") + rgb[1].to_bytes(1, "big")
            controller.write(colour)
            print(controller.read(3))
            changed = False

        
        time.sleep(0.005)