#!/usr/bin/python3
# -*- coding: UTF-8 -*-



from s3200 import const, core
from s3200.core import CommunicationError, Frame
from s3200.test.dummy import DummySerial
import logging

logger = logging.getLogger('s3200')

try:
    from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE
except:
    logger.error("WARN: Could not load serial module. Only dummy mode!")

class Connection(object):
    """ A class representing a serial connection to a s3200 device. """

    def __init__(self, serial_port_name="/dev/ttyAMA0"):
        self.serial_port_name = serial_port_name

    def send(self, command: bytes=None, payload: bytes=None):
        """ Shortcut for send_frame. Builds the Frame object and sends it. """

        frame = Frame(command, payload)
        return_frame = self.send_frame(frame)

        return return_frame

    def open_serial(self):
        """Opens a serial port and returns it."""
        if self.serial_port_name == 'dummy':
            serial_port = DummySerial()
        else:
            serial_port = Serial(self.serial_port_name, 57600, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, timeout=3)
        return serial_port

    def send_frame(self, frame, read_answer_frames=1):
        """ Sends one frame and receives the answer frame

        :param frame: the frame to send
        :return frame: the answer frame
        :raise: different exceptions that could occur during communication
        """

        serial_port = self.open_serial()
        answer_frames = []

        try:
            #send the frame
            logger.debug('sending: ' + str(frame.to_bytes()))
            serial_port.write(frame.to_bytes())

            #read the answer bytes
            for i in range(read_answer_frames):
                answer_bytes = Connection._read_one_frame(serial_port)
                logger.debug('read answer:' + str(answer_bytes))
                #wrong set_setting returns 2x -> logger.info("'"+str(core.convert_bytes_to_hex(frame.to_bytes()))+"'"+': ' + str(answer_bytes)+',')
                #make a frame from the bytes
                answer_frame = Frame.from_bytes(answer_bytes)
                answer_frames.append(answer_frame)

        except core.NothingToReadError as e:
            serial_port.flushInput()
            raise core.WrongNumberOfAnswerFramesError("Got wrong no of answer frames",
                                                      read_answer_frames, len(answer_frames), e)

        finally:
            serial_port.close()

        if len(answer_frames) > 1:
            return answer_frames
        else:
            return answer_frames[0]

    @staticmethod
    def _read_one_frame(serial_port):

        frame_start_bytes = serial_port.read(2)

        if serial_port.inWaiting() == 0:
            raise core.NothingToReadError("No Bytes to Read")

        #get length
        length_bytes = Connection._read_escaped(serial_port, 2)
        unescaped_length_bytes = core.unescape(length_bytes)
        if len(unescaped_length_bytes) != 2:
            raise core.CommunicationError("Didn't get 2 length bytes. Maybe timeout, or other reading error.")

        length = core.convert_short_to_integer(unescaped_length_bytes)

        read_bytes = Connection._read_escaped(serial_port, length + 1)  # +1 for read the checksum too
        complete_frame = frame_start_bytes + length_bytes + read_bytes

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

    def get_list(self, command_start_address: bytes, command_next_address: bytes, max_loops=500):
        """ Get all items of a list """

        output = []
        answer_frame = self.send(command_start_address)

        while answer_frame.payload != b'\x00' :  # TODO add constant
            logger.debug('get_list payload: ' + str(answer_frame.payload))

            if answer_frame.payload == b'\x01' :
                logger.debug('ignore payload: ' + str(answer_frame.payload))
            else:
                output.append(answer_frame)

            answer_frame = self.send(command_next_address, b'\x01')
            logger.debug('get_list len: ' + str(len(output)))

            #prevent endless loops
            if len(output) > max_loops:
                raise ValueError("Reached max_loops: " + str(max_loops))

        return output