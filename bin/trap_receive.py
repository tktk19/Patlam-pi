#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os, sys
import RPi.GPIO as GPIO
import time

# import main flask project
my_path = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.normpath(os.path.join(my_path, '../'))
sys.path.append(main_path)
import patlam_pi

import logging
import logging.handlers

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

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        __formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        __handler = logging.handlers.RotatingFileHandler(
            filename=patlam_pi.app.config['LOGFILE'],
            maxBytes=102400,
            backupCount=10,
        )
        __handler.setFormatter(__formatter)
        self.logger.addHandler(__handler)

    def __sound(self):
        sound_file = os.path.join(patlam_pi.app.config['SOUNDDATA'], "ALARM.WAV")
        self.log('SoundPlay Start : ' + sound_file)
        cmd = "/usr/bin/aplay " + sound_file + " &"
        os.system(cmd)
        self.log('SoundPlay End')

    def __light(self):
        __led_blink_count = patlam_pi.get_setting('LEDBlink')
        self.log('LED blink ' + __led_blink_count + ' Times Start')
        i = 0
        while i < int(__led_blink_count):
            GPIO.output(23, True)
            GPIO.output(24, True)
            time.sleep(0.5)
            GPIO.output(23, False)
            GPIO.output(24, False)
            time.sleep(0.5)
            i+=1
            
        self.log('LED blink Stop')

    def fire(self):
        self.__sound()
        self.__light()

    def log(self, string):
        self.logger.debug(string)

if __name__ == '__main__':
    alart = Alart()
    alart.log(' '.join(sys.argv))
    patlam_pi.set_volume()
    alart.fire()