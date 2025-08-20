#!/usr/bin/env python
import io
import serial
from time import sleep

# COM Class handles serial connections
class Com():
    def __init__(self, port='/dev/ttyUSB0', baud=115200, limit=0.1):
        self.con = serial.Serial(port, baud, timeout=limit)
        self.sout = io.TextIOWrapper(io.BufferedWriter(self.con),encoding="ascii")
        self.sin = io.TextIOWrapper(io.BufferedReader(self.con),encoding="ascii")

    def write(self, text, newline = True):
        for ltr in f'{text}':
            self.sout.write(f'{ltr}')
            self.sout.flush()
            sleep(0.01)
        if newline:
            self.sout.write('\r')
            self.sout.flush()
            sleep(0.01)

    def read(self):
        return self.sin.readlines()

    def print(self):
        for line in self.sin.readlines():
            print(line, end='')
        print('')
        self.sin.flush()
