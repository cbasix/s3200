#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from s3200 import constants, core
from s3200.core import CommunicationError
from s3200.test.dummy import DummySerial


class Frame(object):
    """ An class representing a s3200 communication frame.

    Example:
    To get the operating hours the following frame must be send:
    02 FD 00 03 30 00 62 F2
    02 FD -> Frame start sequence
    00 03 -> Amount of bytes (command + payload)
    30    -> Command (in this case the command for 'get value')
    00 62 -> Payload (in this case the address of the operating hours)
    F2    -> Checksum

    """

    #---CONSTRUCTORS---
    def __init__(self, command: bytes=None, payload: bytes=None):
        self.command = command
        self.payload = payload

        if self.command is None:
            raise core.FrameSyntaxError("Frame must have a command.")

    @staticmethod
    def from_bytes(frame_bytes: bytes):
        """ Get a frame object from its byte representation.

        :param frame_bytes: a frame in byte form
        """

        #example frame (in hex) 02 fd 00 03 30 00 30 04
        start_bytes = frame_bytes[:2]  # 02 fd

        #unescape
        escaped_content = frame_bytes[2:]  # 00 03 30 00 30 04
        unescaped_content = core.unescape(escaped_content)  # 00 03 30 00 30 04 this example has no escaped content

        #get values from unescaped 
        length_bytes = unescaped_content[:2]  # 00 03
        command_byte = unescaped_content[2:3]  # 30
        payload_bytes = unescaped_content[3:-1]  # 00 30
        checksum_byte = unescaped_content[-1:]  # 04

        #check start bytes
        if not start_bytes == constants.START_BYTES:
            raise CommunicationError("Start bytes must be: {0} but are: {1}".format(
                core.get_hex_from_byte(constants.START_BYTES),
                core.get_hex_from_byte(start_bytes)))

        #check checksum
        calculated_checksum = core.calculate_checksum(start_bytes + length_bytes + command_byte + payload_bytes)

        if not checksum_byte[0] == calculated_checksum[0]:
            raise CommunicationError(
                "Checksum byte doesnt match. Received:{0} Calculated:{1}".format(
                    core.get_hex_from_byte(checksum_byte), core.get_hex_from_byte(calculated_checksum)))

        #build return frame
        return Frame(command_byte, payload_bytes)

    #---METHODS---
    def to_bytes(self):
        """ Convert a frame object to its send ready byte representation. """
        #calculate length
        length_bytes = core.get_short_from_integer(len(self.command) + len(self.payload))

        #calculate checksum
        checksum = core.calculate_checksum(constants.START_BYTES + length_bytes + self.command + self.payload)

        #escape all except the start bytes
        content_unescaped = length_bytes + self.command + self.payload + checksum
        content_escaped = core.escape(content_unescaped)

        #build final frame
        frame = constants.START_BYTES + content_escaped

        return frame

    def __str__(self):
        return "<Frame command:{0} payload:{1}>".format(core.get_hex_from_byte(self.command),
                                                        core.get_hex_from_byte(self.payload))


class Connection(object):
    """ A class representing a serial connection to a s3200 device. """

    def __init__(self, serial_port_name="/dev/ttyAMA0"):
        self.serial_port_name = serial_port_name

    def send_request(self, frame):
        """ Sends one frame and receives the answer frame

        :param frame: the frame to send
        :return frame: the answer frame
        :raise: different exceptions that could occur during communication
        """

        if self.serial_port_name == 'dummy':
            serial_port = DummySerial()
        else:
            serial_port = Serial(self.serial_port_name, 57600, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, timeout=3)

        try:
            #send the frame
            #print(convertToHexStr(frame.toBytes()))
            serial_port.write(frame.to_bytes())

            #read the answer bytes
            answer_bytes = Connection._read_one_frame(serial_port)

            #make a frame from the bytes
            answer_frame = Frame.from_bytes(answer_bytes)

        except Exception as e:
            serial_port.flushInput()
            raise e

        finally:
            serial_port.close()

        return answer_frame

    @staticmethod
    def _read_one_frame(serial_port):

        frame_start_bytes = serial_port.read(2)

        #get length
        length_bytes = serial_port.read(2)

        if len(length_bytes) != 2:
            raise IOError("Didn't get length bytes. Maybe timeout, or other reading error.")

        length = core.get_integer_from_short(length_bytes)  # lengthBytes[-1]

        #print('byte:'+str(lengthBytes)+' length:'+str(length))
        #get command

        # read until length is reached and pay attention to escaped bytes
        to_read = length + 1  # +1 is for reading the checksum too
        read_count = 0
        read_bytes = bytearray()

        while read_count < to_read:
            # read one byte and check if it is a escaped one
            read_byte = serial_port.read(1)[0]

            # if the current byte is an escape identifier we need to read one byte more
            if read_byte in constants.ESCAPED_IDENTIFIER:
                to_read += 1

            # append to content array and increase read_count
            read_bytes.append(read_byte)
            read_count += 1

        # reassemble complete frame
        complete_frame = frame_start_bytes + length_bytes + read_bytes

        # print(convertToHexStr(completeFrame))

        return complete_frame
