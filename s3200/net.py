#!/usr/bin/python3
# -*- coding: UTF-8 -*-
try:
    from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
except:
    print("WARN: Could not load serial module. Only dummy mode!")


from s3200 import const, core
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

        if self.payload is None:
            self.payload = b''

        if self.command is None or len(self.command) < 1:
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
        if not start_bytes == const.START_BYTES:
            raise CommunicationError("Start bytes must be: {0} but are: {1}".format(
                core.convert_byte_to_hex(const.START_BYTES),
                core.convert_byte_to_hex(start_bytes)))

        #check checksum
        calculated_checksum = core.calculate_checksum(start_bytes + length_bytes + command_byte + payload_bytes)

        #if len(payload_bytes) > 0:
        if not checksum_byte[0] == calculated_checksum[0]:
            raise CommunicationError(
                "Checksum byte doesnt match. Received:{0} Calculated:{1}. Complete frame:{2}".format(
                    core.convert_byte_to_hex(checksum_byte), core.convert_byte_to_hex(calculated_checksum),
                    core.convert_byte_to_hex(frame_bytes)))

        #build return frame
        return Frame(command_byte, payload_bytes)

    #---METHODS---
    def to_bytes(self):
        """ Convert a frame object to its send ready byte representation. """

        #None should be handled like no byte
        if self.payload is None:
            self.payload = b''

        #calculate length
        length = len(self.command) + len(self.payload)

        length_bytes = core.convert_integer_to_short(length)

        #calculate checksum
        checksum = core.calculate_checksum(const.START_BYTES + length_bytes + self.command + self.payload)

        #escape all except the start bytes
        content_unescaped = length_bytes + self.command + self.payload + checksum
        content_escaped = core.escape(content_unescaped)

        #build final frame
        frame = const.START_BYTES + content_escaped

        return frame

    def __str__(self):
        return "<Frame command:{0} payload:{1}>".format(core.convert_byte_to_hex(self.command),
                                                        core.convert_byte_to_hex(self.payload))


class Connection(object):
    """ A class representing a serial connection to a s3200 device. """

    def __init__(self, serial_port_name="/dev/ttyAMA0"):
        self.serial_port_name = serial_port_name

    def send(self, command: bytes=None, payload: bytes=None):
        """ Shortcut for send_frame. Builds the Frame object and sends it. """

        frame = Frame(command, payload)
        return_frame = self.send_frame(frame)

        return return_frame

    def send_frame(self, frame):
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
        length_bytes = Connection._read_escaped(serial_port, 2)
        unescaped_length_bytes = core.unescape(length_bytes)
        if len(unescaped_length_bytes) != 2:
            raise core.CommunicationError("Didn't get 2 length bytes. Maybe timeout, or other reading error.")

        length = core.convert_short_to_integer(unescaped_length_bytes)

        read_bytes = Connection._read_escaped(serial_port, length + 1)  # +1 for read the checksum too
        complete_frame = frame_start_bytes + length_bytes + read_bytes

        # print(convertToHexStr(completeFrame))

        return complete_frame

    @staticmethod
    def _read_escaped(serial_port, length):
        my_byte = bytearray()

        for i in range(length):
            byte = serial_port.read(1)[0]
            my_byte.append(byte)

            if byte in const.ESCAPED_IDENTIFIER:
                second_byte = serial_port.read(1)[0]
                my_byte.append(second_byte)

        return bytes(my_byte)

    def get_list(self, command_start_address: bytes, command_next_address: bytes):
        """ Get all items of a list """

        output = []
        answer_frame = self.send(command_start_address)

        while len(answer_frame.payload) > 0:
            output.append(answer_frame)

            answer_frame = self.send(command_next_address)

        return output