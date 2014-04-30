#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from collections import OrderedDict

import re
from s3200 import core


# noinspection PyPep8Naming,PyPep8Naming
class DummySerial(object):
    """ A dummy serial port implementation that behaves like a simplified connected s3200 """

    COMM_LIST = OrderedDict({
        # value working hours answer 55
        '02 FD 00 03 30 00 62 F2': b'\x02\xfd\x00\x030\x007\r',
        # simulate transmission error wrong checksum when asked for 00 59 heater_circuit_18_is
        '02 FD 00 03 30 00 59 BF': b'\x02\xfd\x00\x02\x000\x10h',
        # other values answer 4322
        '02 FD .. .. 30 (?!(00 62 F2))(?!(00 59 BF)).*': b'\x02\xFD\x00\x03\x30\x10\xE2\x42',
        # answer to 22 test
        '02 FD .. .. 22 .*': 'return',
        # answer to 41 sw version and current datetime
        '02 FD .. .. 41 .*': b'\x02\xFD\x00\x0C\x41\x50\x04\x04\x14\x00\x1F\x12\x15\x0B\x07\x0A\x38',
        # error buffer get_error
        '02 FD .. .. 47 .*': b'\x02\xfd\x009G\x01\x00m\xa3\x01\x02\x00\xfe\x12\x0c\x04\x02\x00\x0c' +
                             b'Z\xfcndversuch nicht gelungen von Hand Anheizen!\xbc',
        # error buffer get_next_error EMPTY
        '02 FD .. .. 48 .*': b'\x02\xfd\x00\x01\x48\xda',
                            #b'\x02\xFD\x00\x02\x47\xCE',
                             #b'\x02\xFD\x00\x02\x00\x47\x00\xCE'
        #get configuration
        '02 FD .. .. 40 .*': b'\x02\xFD\x00\x59\x40\x00\x00\x00\x04\x00\x24\x00\x03\x00\x00\x00' +
                             b'\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00' +
                             b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00' +
                             b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00' +
                             b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                             b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x49',
        #get_heater_state_and_mode
        '02 FD .. .. 51 .*': b'\x02\xFD\x00\x18\x51\x02\x00\x00\xDC\x62\x65\x72\x67\x61\x6E\x67' +
                             b'\x73\x62\x65\x74\x72\x3B\x53\x54\xD6\x52\x55\x4E\x47\x8C',
        #menu item start
        '02 FD .. .. 37 .*': b'\x02\xFD\x00\x44\x37\x01\x07\x00\x01\x72\x00\x00\x04\x00\x00\x00'
                             b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x53'
                             b'\x00\xF7\x50\x72\x6F\x70\x6F\x72\x74\x69\x6F\x6E\x61\x6C\x66\x61'
                             b'\x6B\x74\x6F\x72\x20\x64\x65\x73\x20\x4D\x69\x73\x63\x68\x65\x72'
                             b'\x72\x65\x67\x6C\x65\x72\x73\x00\x7D',
 
        #menu next item empty
        '02 FD .. .. 38 .*': b'\x02\xfd\x00\x018J',
    })

    def __init__(self, port=None, baud_rate=None, eight_bits=None, parity=None, stop_bits=None, timeout=None):
        self.in_buffer = bytearray()
        self.out_buffer = bytearray()

    def flushInput(self):
        self.do_processing()

    def close(self):
        self.in_buffer = bytearray() #  .clear()
        self.out_buffer = bytearray() #  .clear()

    def write(self, write_bytes: bytes):
        for b in write_bytes:
            self.out_buffer.append(b)
        self.do_processing()

    def read(self, length=1):
        """dummy read function
        :param length: bytes to read
        """
        ret = self.in_buffer[0:length]
        self.in_buffer = self.in_buffer[length:]
        return ret

    def do_processing(self):
        for key, value in DummySerial.COMM_LIST.items():
            r = re.compile(key)
            hex_string = core.get_hex_from_byte(bytes(self.out_buffer)).upper()
            if r.match(hex_string):

                if value == 'return':
                    value = bytes(self.out_buffer)

                self.out_buffer = bytearray() #  .clear()

                for i in value:
                    self.in_buffer.append(i)
                print("Dummy in: {0} out: {1}".format(str(hex_string), str(value)))
                return

