#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from collections import OrderedDict
from s3200 import constants, core, net


class S3200(object):
    """ A class representing a s3200 object. """

    def __init__(self, serial_port_name="/dev/ttyAMA0",
                 value_address=constants.VALUE_ADDRESS,
                 value_address_group=constants.VALUE_ADDRESS_GROUP,
                 command_address=constants.COMMAND_ADDRESS):

        self.connection = net.Connection(serial_port_name=serial_port_name)
        self.value_address = value_address
        self.value_address_group = value_address_group
        self.command_address = command_address


    def get_value_list(self, group=None, with_local_name=False):

        actual_values = OrderedDict()
        if group is None:
            entry_list = self.value_address
        else:
            entry_list = self.value_address_group[group]

        for group_item in entry_list:
            actual_values[group_item] = self.get_value(group_item, with_local_name)

        return actual_values

    def get_value(self, value_name: str, with_local_name: bool=False):
        """ Get value by name.

        :param with_local_name: if yes output is a tuple with (name, value) instead of value only
        :param value_name: name of the value as specified in address_dict
        """

        if not self.value_address[value_name]:
            raise core.ValueAddressNotDefinedError("Address for value: '{0}' not defined in address_dict".format(value_name))

        if not self.command_address['get_value']:
            raise core.CommandAddressNotDefinedError("Address for command: 'get_value' not defined in command_dict")

        value_d = self.value_address[value_name]

        # Prepare the frame and get the answer
        command_addr = self.command_address['get_value']['address']
        val_addr = value_d['address']

        send_frame = net.Frame(command_addr, val_addr)
        answer_frame = self.connection.send_request(send_frame)

        value = core.get_integer_from_short(answer_frame.payload)
        value = value / value_d['factor']

        if not with_local_name:
            return value
        else:

            return_list = (value_d['local_name'], value)
            return return_list
