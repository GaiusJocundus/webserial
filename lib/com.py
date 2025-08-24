#!/usr/bin/env python
import io
import serial
from time import sleep
import asyncio
import serial_asyncio

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

# ComProtocol Class handles async connection
class ComProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print('data received', repr(data))
        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing') 

def main():
	loop = asyncio.get_event_loop()
	coro = serial_asyncio.create_serial_connection(loop, ComProtocol, '/dev/ttyUSB0', baudrate=115200)
	transport, protocol = loop.run_until_complete(coro)
	loop.run_forever()
	loop.close()

if __name__ == '__main__':
	main()
