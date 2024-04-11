#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time


#Set function to calculate percent from angle
def angle_to_percent(angle):
    if angle > 180 or angle < 0:
        return False
    else:
        start = 4
        end = 12.5
        ratio = (end - start) / 180  # Calcol ratio da angolo a percentuale

        angle_as_percent = angle * ratio
        if angle_as_percent > end:  # Assicura che il valore non superi il limite massimo
            angle_as_percent = end

    return start + angle_as_percent



pwm1_gpio = 13
pwm2_gpio = 14
frequence = 50

