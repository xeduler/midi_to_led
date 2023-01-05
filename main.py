#!/usr/bin/python
import serial
import time
import pygame
import pygame.midi

pygame.midi.init()
keyboard = pygame.midi.Input(3, 1000)

rgb = [0, 0, 0]
changed = False



# settings
mcu_port = "/dev/ttyACM0"
mcu_baudrate = 115200

MIDI_brightness = 176

# default parameters
mode = 1
bright = 0.5
max_brightness = 200
min_brightness = 10
fade_speed = 0.4 # <= min_brightness

# MIDI keyboard ranges
range_red_start   = 20
range_red_end     = 54
range_green_start = 54
range_green_end   = 75
range_blue_start  = 75
range_blue_end    = 108






with serial.Serial(port = mcu_port, baudrate = mcu_baudrate, timeout = 1) as controller:
    time.sleep(3)

    while 1:   
        if(pygame.midi.Input.poll(keyboard)):
            midi_data = pygame.midi.Input.read(keyboard, 1)[0][0]
            if midi_data[0] == 144: # Note played
                note = midi_data[1]
                power = midi_data[2]
                #print(midi_data)
                if note > range_red_start and note <= range_red_end:
                    rgb[0] = rgb[0] + power * bright
                    if rgb[0] > max_brightness:
                        rgb[0] = max_brightness
                elif note > range_green_start and note <= range_green_end:
                    rgb[1] = rgb[1] + power * bright
                    if rgb[1] > max_brightness:
                        rgb[1] = max_brightness
                elif note > range_blue_start and note <= range_blue_end:
                    rgb[2] = rgb[2] + power * bright
                    if rgb[2] > max_brightness:
                        rgb[2] = max_brightness
            elif midi_data[0] == MIDI_brightness: # Brightness controller event
                if midi_data[1] == 1:
                    bright = midi_data[2] / 127

        if rgb[0] >= min_brightness:
            rgb[0] -= fade_speed
            changed = True
        if rgb[1] >= min_brightness:
            rgb[1] -= fade_speed
            changed = True
        if rgb[2] >= min_brightness:
            rgb[2] -= fade_speed
            changed = True
        
        if changed == True:
            colour = int(rgb[2]).to_bytes(1, "big") + int(rgb[0]).to_bytes(1, "big") + int(rgb[1]).to_bytes(1, "big") + mode.to_bytes(1, "big")
            controller.write(colour)
            changed = False
            #print(controller.read(3))

        
        time.sleep(0.005)