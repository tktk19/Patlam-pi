#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import RPi.GPIO as GPIO
import time

# import main flask project
sys.path.append(os.getcwd())
import patlam_pi

u"""
snmp_trap 受信時のアラートを実施
UI側で設定したアラート音声やLEDの点滅回数を実施する

"""

class Alart():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)

    def __sound(self):
        sound_file = os.path.join(patlam_pi.app.config['SOUNDDATA'], "ALARM.WAV")
        cmd = "/usr/bin/aplay " + sound_file + " &"
        os.system(cmd)

    def __light(self):
        i = 0
        while i < 5:
            GPIO.output(23, True)
            GPIO.output(24, True)
            time.sleep(0.5)
            GPIO.output(23, False)
            GPIO.output(24, False)
            time.sleep(0.5)
            i+=1

    def fire(self):
        self.__sound()
        self.__light()

if __name__ == '__main__' :
    alart = Alart()
    alart.fire()