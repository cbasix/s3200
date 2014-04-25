#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from s3200 import core


class DummySerial(object):
    """ A dummy serial port implementation that behaves like a simplified connected s3200 """

    COMM_LIST = {
        # value working hours answer 55
        '02 FD 00 03 30 00 62 F2': b'\x02\xfd\x00\x030\x007\r',
        # simulate transmission error wrong checksum when asked for 00 59 heater_circuit_18_is
        '02 FD 00 03 30 00 59 BF': b'\x02\xfd\x00\x02\x000\x10h',
        # other values answer 4322
        '02 FD .. .. 30 (?!(00 62 F2)).*': b'\x02\xFD\x00\x03\x30\x10\xE2\x42',

    }

    def __init__(self, port=None, baud_rate=None, eight_bits=None, parity=None, stop_bits=None, timeout=None):
        self.in_buffer = bytearray()
        self.out_buffer = bytearray()

    def flushInput(self):
        self.do_processing()

    def close(self):
        self.in_buffer.clear()
        self.out_buffer.clear()

    def write(self, write_bytes: bytes):
        for b in write_bytes:
            self.out_buffer.append(b)
        self.do_processing()

    def read(self, length=1):
        """dummy read function"""
        ret = self.in_buffer[0:length]
        self.in_buffer = self.in_buffer[length:]
        return ret

    def do_processing(self):
        for key, value in DummySerial.COMM_LIST.items():
            r = re.compile(key)
            hex_string = core.get_hex_from_byte(bytes(self.out_buffer)).upper()
            if r.match(hex_string):
                self.out_buffer.clear()
                for i in value:
                    self.in_buffer.append(i)
                return
