#!/usr/bin/python
import serial
import time
import pygame
import pygame.midi

pygame.midi.init()
keyboard = pygame.midi.Input(1, 1000)

rgb = [0, 0, 0, 0]
changed = False



# settings
mcu_port = "/dev/ttyACM0"
mcu_baudrate = 115200

MIDI_brightness = 1
MIDI_max_brightness = 2
MIDI_min_brightness = 3
MIDI_fade = 4

# default parameters
mode = 1
bright = 0.2
max_brightness = 255
min_brightness = 1
fade_speed = 1 # <= min_brightness

# MIDI keyboard ranges
range_red_start   = 20
range_red_end     = 54
range_green_start = 54
range_green_end   = 75
range_blue_start  = 75
range_blue_end    = 108

range_ceil_start  = 108
range_ceil_end    = 110






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
                elif note > range_ceil_start and note <= range_ceil_end:
                    rgb[3] = rgb[3] + power * bright
                    if rgb[3] > max_brightness:
                        rgb[3] = max_brightness
            elif midi_data[0] == 176:                 # Controller event
                if midi_data[1] == MIDI_brightness:       # Brightness controller event
                    bright = midi_data[2] / 127
                elif midi_data[1] == MIDI_max_brightness: # Max brightness controller event
                    max_brightness = (midi_data[2] * 2) + 1
                    if max_brightness < min_brightness:
                        max_brightness = min_brightness + 1
                elif midi_data[1] == MIDI_min_brightness: # Min brightness controller event
                    min_brightness = (midi_data[2] * 2) - 1
                    if min_brightness > max_brightness:
                        min_brightness = max_brightness - 1
                elif midi_data[1] == MIDI_fade:           # Fade speed controller event
                    fade_speed = midi_data[2]
                    if fade_speed > min_brightness:
                        fade_speed = min_brightness
                    


        if rgb[0] >= min_brightness:
            rgb[0] -= fade_speed
            changed = True
        if rgb[1] >= min_brightness:
            rgb[1] -= fade_speed
            changed = True
        if rgb[2] >= min_brightness:
            rgb[2] -= fade_speed
            changed = True
        if rgb[3] >= min_brightness:
            rgb[3] -= fade_speed
            changed = True
        
        if changed == True:
            colour = int(rgb[3]).to_bytes(1, "big") + int(rgb[2]).to_bytes(1, "big") + int(rgb[0]).to_bytes(1, "big") + int(rgb[1]).to_bytes(1, "big") + mode.to_bytes(1, "big")
            controller.write(colour)
            changed = False
            #print(controller.read(3))

        
        time.sleep(0.005)