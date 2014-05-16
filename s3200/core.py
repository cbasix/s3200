#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
import string

from s3200 import const
from collections import OrderedDict
from datetime import datetime, time
import logging

#---LOGGING---
# create logger with 'spam_application'
logger = logging.getLogger('s3200')
logger.setLevel(logging.WARN)
# create file handler which logs even debug messages
#fh = logging.FileHandler('input_output.log')
#fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
#logger.addHandler(fh)
logger.addHandler(ch)


#---HELPER METHODS---
def calculate_checksum(data_bytes: bytes):
    """ Calculates the checksum of the given data.

    :param data_bytes:
    """
    crc = 0x00

    for aByte in data_bytes:
        temp = (aByte * 2) & 0xFF
        crc = crc ^ aByte ^ temp

    return bytes([crc])


def convert_bytes_to_datedaytime(date_bytes: bytes):
    """ Get a date object from its 7byte representation.

    :param date_bytes: the 7 byte long representation of a date

        Form:
        seconds minutes hours day month weekday year

        Example:
        00 1F 12 15 0B 07 0A
        Time: 00 1F 12 -> 18:31:00
        Date: 15 0B 07 0A -> 21.11.; 7. Day of week = Sunday ; (20)10
    """

    date_array = const.StructDateDayTime.unpack(date_bytes)

    second = date_array[0]
    minute = date_array[1]
    hour = date_array[2]
    day = date_array[3]
    month = date_array[4]
    # weekday = date_array[5] # 1=Monday 7=Sunday
    year = 2000 + date_array[6]  # 2000 + byte

    return datetime(year, month, day, hour, minute, second)


def get_bytes_from_date_day_time(datetime_to_set: datetime):
    """ Get the 7byte representation of a date object.
    """

    date_list = []

    date_list.append(datetime_to_set.second)
    date_list.append(datetime_to_set.minute)
    date_list.append(datetime_to_set.hour)
    date_list.append(datetime_to_set.day)
    date_list.append(datetime_to_set.month)
    date_list.append(datetime_to_set.isoweekday())  # 1=Monday 7=Sunday
    date_list.append(datetime_to_set.year - 2000)  # 2000 + byte

    date_bytes = const.StructDateDayTime.pack(date_list)

    return date_bytes

def convert_byte_to_datetime(date_bytes: bytes):
    """ Get a date object from its 6byte representation.

    :param date_bytes: the 6 byte long representation of a date

        Form:
        seconds minutes hours day month weekday year

        Example:
        00 1F 12 15 0B 07 0A
        Time: 00 1F 12 -> 18:31:00
        Date: 15 0B 0A -> 21.11.(20)10
    """

    date_array = const.StructDateTime.unpack(date_bytes)

    second = date_array[0]
    minute = date_array[1]
    hour = date_array[2]
    day = date_array[3]
    month = date_array[4]
    year = 2000 + date_array[5]  # 2000 + byte

    return datetime(year, month, day, hour, minute, second)


def convert_short_to_integer(short_bytes: bytes):
    """ Get a integer of its 2byte representation.

    :param short_bytes: two bytes representing a short
    """

    # allow to convert single byte values
    if len(short_bytes) == 1:
        short_bytes = b'\x00' + short_bytes

    if len(short_bytes) != 2:
        raise ShortUnpackError("2bytes input needed {0}bytes given".format(len(short_bytes)))

    temp_array = const.StructShort.unpack(short_bytes)
    integer = temp_array[0]

    return integer


def convert_integer_to_short(integer: int):
    """ Get the 2byte representation of an integer.

    :param integer: an int to convert to a short. Max. 65025
    """

    if integer < 0 or integer > 65025:
        raise ShortPackError("Given value: {0} could not be represented as 2byte short. " +
                             "Allowed: 0 < value < 65025".format(integer))

    temp_bytes = const.StructShort.pack(integer)

    return temp_bytes


def convert_bytes_to_string(byte_data: bytes):
    """ String from bytes.

    :param byte_data: data to convert
    """

    string_data = byte_data.decode(encoding='cp1252')
    return string_data


def convert_string_to_bytes(string_data: str):
    """ Bytes from string.

    :param string_data: data to convert
    """

    byte_data = string_data.encode(encoding='cp1252')
    return byte_data


def convert_bytes_to_hex(byte_data: bytes):
    """ Convert bytes to a hex string of format 0A FD C3.

    :param byte_data: the byte data to convert to hex
    """
    return ' '.join(['{:02x}'.format(i) for i in byte_data])


def get_flag_from_bytes(data_bytes: bytes, position: int):
    return is_flag_set(data_bytes, position_from_left=position)


def convert_bytes_to_error(error_bytes: bytes):
    """ Get an error dict from bytes representation. """

    return_dict = convert_structure_to_dict(error_bytes, const.ERROR_STRUCTURE)

    return return_dict


def convert_bytes_to_menu_item(menu_item_bytes: bytes):

    # load the definition (what is where) from the constants
    address_def = const.MENU_ITEM_STRUCTURE['address']
    text_def = const.MENU_ITEM_STRUCTURE['text']

    # get the data from their position in the byte data
    address = menu_item_bytes[address_def['start']:address_def['end']]
    text = convert_bytes_to_string(menu_item_bytes[text_def['start']:text_def['end']])

    #build the return dict
    return_dict = {
        'address': address,
        'text': text,
    }

    return return_dict


def convert_bytes_to_configuration(configuration_bytes: bytes):
    return convert_structure_to_dict(configuration_bytes, const.CONFIGURATION_STRUCTURE)



def convert_structure_to_dict(data_bytes, configuration_dict):

    logger.debug('Loaded structure dict: ' + str(configuration_dict) + ' for usage on: ' + str(data_bytes))

    return_dict = {}
    for structure_name, structure_data in configuration_dict.items():

        assert isinstance(structure_data, dict)

        logger.debug('LoadStructure: ' + structure_name )

        structure_type = structure_data['type']
        structure_bytes = data_bytes[structure_data['start']:structure_data['end']]

        logger.debug('Structure extracted bytes: ' + str(structure_bytes))
        value = None

        if structure_type == 'short':
            value = convert_short_to_integer(structure_bytes)

        elif structure_type == 'bytes':
            value = bytes(structure_bytes)

        elif structure_type == 'datetime':
            value = convert_byte_to_datetime(structure_bytes)

        elif structure_type == 'string':
            value = str(convert_bytes_to_string(structure_bytes))

        elif structure_type == 'flag':
            value = bool(get_flag_from_bytes(structure_bytes, structure_data['bit']))

        elif structure_type == 'time10':
            value = convert_bytes_to_time10(structure_bytes)

        # if it is a reference the value should come from the referenced item
        if 'reference' in structure_data:
            reference_dict = structure_data['reference']
            try:
                value = reference_dict[value]
            except KeyError as e:
                raise ReferenceValueNotInConst(str(e)) from e

        logger.debug('Structure converted data: ' + str(value))

        return_dict[structure_name] = value

    return return_dict


def convert_bytes_to_time10(data_bytes):
    data_int = convert_short_to_integer(data_bytes)  # 96h = 150d 0 15:00

    if data_int == 255:  # FFh -> no time set
        return None
    elif data_int > 240:
        raise InvalidValueError('Time value must be between 0 and 240')

    data_str = str(data_int)  # "150"

    hours = int(data_str[:2])  # 15
    minutes = int(data_str[2:]) * 10  # 0 -> time10 has only 10minutes resolution

    return_value = time(hours, minutes)
    return return_value


def convert_bytes_to_state_and_mode(state_mode_bytes: bytes):
    state_and_mode = convert_structure_to_dict(state_mode_bytes, const.STATE_AND_MODE_STRUCTURE)
    state_and_mode_string = state_and_mode['text']

    state_mode_tuple = state_and_mode_string.split(';')
    mode = state_mode_tuple[0]
    state = state_mode_tuple[1]

    return state, mode


def convert_bytes_to_state(state_mode_bytes: bytes):
    state, mode = convert_bytes_to_state_and_mode(state_mode_bytes)
    return state


def convert_bytes_to_mode(state_mode_bytes: bytes):
    state, mode = convert_bytes_to_state_and_mode(state_mode_bytes)
    return mode


def convert_bytes_to_setting(payload: bytes):
    return convert_structure_to_dict(payload, const.SETTING_STRUCTURE)


def convert_bytes_to_available_value(payload: bytes):
    return convert_structure_to_dict(payload, const.AVAILABLE_VALUE_STRUCTURE)

def convert_time_slot_to_bytes(item, weekday, time_slot_1_start, time_slot_1_end, time_slot_2_start, time_slot_2_end,
                             time_slot_3_start, time_slot_3_end, time_slot_4_start, time_slot_4_end):

    raise NotImplementedError
    #return data_bytes

def is_flag_set(flag_data_bytes: bytes, position_from_left):
    bin_string = ""
    for byte in flag_data_bytes:
        temp = bin(byte)[2:]  # cut off 0b prefix
        temp = '00000000' + temp  # fill up with 0
        temp = temp[-8:]  # get the last 8
        bin_string += temp

    #print('bin_string len: ' + str(len(bin_string)) + ' asked position: ' + str(position_from_left))
    return bool(bin_string[position_from_left] == '1')


def escape(data: bytes):
    """ Escape the given data according to the s3200 documentation.

    :param data: the bytes to escape
    """
    return replace_all(data, const.ESCAPE_LIST)


def unescape(data):
    """ Unescape the given data according to the s3200 documentation.

    :param data: the bytes to unescape
    """

    return replace_all(data, const.UNESCAPE_LIST)


def replace_all(data: bytes, dic: OrderedDict):
    """ Replaces all occurrences of a byte.

    :param data: The original bytes
    :param dic: The OrderedDict with the original and the replace values
    """

    for i, j in dic.items():
        data = data.replace(i, j)
    return data


def get_random_string(size=10, chars=string.ascii_letters + string.digits):
    """ Get random string.

    :param size: length of the random string
    :param chars: chars the random string should contain default is ascii_letters + digits
    """
    return ''.join(random.choice(chars) for _ in range(size))


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
            raise FrameSyntaxError("Frame must have a command.")

    @staticmethod
    def from_bytes(frame_bytes: bytes):
        """ Get a frame object from its byte representation.

        :param frame_bytes: a frame in byte form
        """

        #example frame (in hex) 02 fd 00 03 30 00 30 04
        start_bytes = frame_bytes[:2]  # 02 fd

        #unescape
        escaped_content = frame_bytes[2:]  # 00 03 30 00 30 04
        unescaped_content = unescape(escaped_content)  # 00 03 30 00 30 04 this example has no escaped content

        #get values from unescaped
        length_bytes = unescaped_content[:2]  # 00 03
        command_byte = unescaped_content[2:3]  # 30
        payload_bytes = unescaped_content[3:-1]  # 00 30
        checksum_byte = unescaped_content[-1:]  # 04

        #check start bytes
        if not start_bytes == const.START_BYTES:
            raise CommunicationError("Start bytes must be: {0} but are: {1}".format(
                convert_bytes_to_hex(const.START_BYTES),
                convert_bytes_to_hex(start_bytes)))

        #check checksum
        calculated_checksum = calculate_checksum(start_bytes + length_bytes + command_byte + payload_bytes)

        #if len(payload_bytes) > 0:
        if not checksum_byte[0] == calculated_checksum[0]:
            raise CommunicationError(
                "Checksum byte doesnt match. Received:{0} Calculated:{1}. Complete frame:{2}".format(
                    convert_bytes_to_hex(checksum_byte), convert_bytes_to_hex(calculated_checksum),
                    convert_bytes_to_hex(frame_bytes)))

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

        length_bytes = convert_integer_to_short(length)

        #calculate checksum
        checksum = calculate_checksum(const.START_BYTES + length_bytes + self.command + self.payload)

        #escape all except the start bytes
        content_unescaped = length_bytes + self.command + self.payload + checksum
        content_escaped = escape(content_unescaped)

        #build final frame
        frame = const.START_BYTES + content_escaped

        return frame

    def __str__(self):
        return "<Frame command:{0} payload:{1}>".format(convert_bytes_to_hex(self.command),
                                                        convert_bytes_to_hex(self.payload))


class S3200Error(Exception):
    """Base class for exceptions in this module.

       Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg=''):
        self.msg = msg


class ShortPackError(S3200Error):
    """Exception raised for values that would not fit into the 2byte short."""


class ShortUnpackError(S3200Error):
    """Exception raised for values that would not fit into the 2byte short."""


class FrameSyntaxError(S3200Error):
    """Exception raised when the syntax or value of a frame is not correct."""


class ValueNotDefinedError(S3200Error):
    """Exception raised when the value asked for is not defined id address_dict."""


class CommandNotDefinedError(S3200Error):
    """Exception raised when the command asked for is not defined id command_dict."""


class CommunicationError(S3200Error):
    """Exception raised when the command asked for is not defined id command_dict."""


class ReadonlyError(S3200Error):
    """Exception raised when trying to write a value when S3200 object is in readonly mode."""


class InvalidValueError(S3200Error):
    """ Exception raised when an unusable value is returned.
    """


class ValueSetError(S3200Error):
    """ Exception raised when an error occurred during setting a value
    """


class NothingToReadError(S3200Error):
    """ Exception raised when an error occurred during setting a value
    """

class WrongNumberOfAnswerFramesError(S3200Error):
    """ Exception raised when an error occurred during setting a value
    """
    def __init__(self, msg, expected, got, base_error):
        super().__init__(msg)
        self.expected = expected
        self.got = got
        self.base_error = base_error

class ReferenceValueNotInConst(S3200Error):
    """ Exception raised when value is references that is not defined in const
    """