#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import RPi.GPIO as GPIO

# import main flask project
my_path = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.normpath(os.path.join(my_path, '../'))
sys.path.append(main_path)
import patlam_pi

u"""
/etc/rc.local からキックされる
GPIOのモード設定と音量調節を行った後に
IPアドレスを音声で読み上げる
"""

def report_ip():
    sound_file = os.path.join(patlam_pi.app.config['SOUNDDATA'], "ALARM.WAV")
    cmd = """\
_IP=$(hostname -I)
if [ "$_IP" ]; then
    /opt/aquestalkpi/AquesTalkPi "起動しました、IPアドレス ${_IP}"  | aplay
else
    /opt/aquestalkpi/AquesTalkPi "起動しました、IPアドレスが割り当てられませんでした"  | aplay
fi
"""
    os.system(cmd)

def init_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

if __name__ == '__main__':
    init_gpio()
    patlam_pi.set_volume_fromdb()
    report_ip()