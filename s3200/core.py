#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from s3200 import constants
from collections import OrderedDict
from datetime import datetime

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


def get_date_from_byte(date_bytes: bytes):
    """ Get a date object from its 7byte representation.

    :param date_bytes: the 7 byte long representation of a date

        Form:
        seconds minutes hours day month weekday year

        Example:
        00 1F 12 15 0B 07 0A
        Time: 00 1F 12 -> 18:31:00
        Date: 15 0B 07 0A -> 21.11.; 7. Day of week = Sunday ; 2010
    """

    date_array = constants.StructDate.unpack(date_bytes)

    second = date_array[0]
    minute = date_array[1]
    hour = date_array[2]
    day = date_array[3]
    month = date_array[4]
    # weekday = date_array[5] # 1=Monday 7=Sunday
    year = date_array[6]

    return datetime(year, month, day, hour, minute, second)


def get_integer_from_short(short_bytes: bytes):
    """ Get a integer of its 2byte representation.

    :param short_bytes: two bytes representing a short
    """

    if len(short_bytes) != 2:
        raise ShortUnpackError("2bytes input needed {0}bytes given".format(len(short_bytes)))

    temp_array = constants.StructShort.unpack(short_bytes)
    integer = temp_array[0]

    return integer


def get_short_from_integer(integer: int):
    """ Get the 2byte representation of an integer.

    :param integer: an int to convert to a short. Max. 65025
    """

    if integer < 0 or integer > 65025:
        raise ShortPackError("Given value: {0} could not be represented as 2byte short. " +
                             "Allowed: 0 < value < 65025".format(integer))

    temp_bytes = constants.StructShort.pack(integer)

    return temp_bytes


def get_hex_from_byte(byte_data: bytes):
    """ Convert bytes to a hex string of format 0A FD C3.

    :param byte_data: the byte data to convert to hex
    """
    return ' '.join(['{:02x}'.format(i) for i in byte_data])


def escape(data: bytes):
    """ Escape the given data according to the s3200 documentation.

    :param data: the bytes to escape
    """
    return replace_all(data, constants.ESCAPE_LIST)


def unescape(data):
    """ Unescape the given data according to the s3200 documentation.

    :param data: the bytes to unescape
    """

    return replace_all(data, constants.UNESCAPE_LIST)


def replace_all(data: bytes, dic: OrderedDict):
    """ Replaces all occurrences of a byte.

    :param data: The original bytes
    :param dic: The OrderedDict with the original and the replace values
    """

    for i, j in dic.items():
        data = data.replace(i, j)
    return data


class S3200Error(Exception):
    """Base class for exceptions in this module.

       Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
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
