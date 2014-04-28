#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from collections import OrderedDict
from s3200 import constants, core, net


class S3200(object):
    """ A class representing a s3200 object. """

    def __init__(self, serial_port_name="/dev/ttyAMA0",
                 value_definitions=constants.VALUE_DEFINITIONS,
                 value_group_definitions=constants.VALUE_GROUP_DEFINITIONS,
                 command_definitions=constants.COMMAND_DEFINITIONS):

        self.connection = net.Connection(serial_port_name=serial_port_name)
        self.value_definitions = value_definitions
        self.value_group_definitions = value_group_definitions
        self.command_definitions = command_definitions

    def get_value_list(self, group=None, with_local_name=False):
        """ Get a list of values.

        :param group: get only values of this group ex. 'heater', or 'boiler_1'
        :param with_local_name: if yes each value returns a tuple with (local_name, value) instead of value only
        """
        return_list = OrderedDict()
        if group is None:
            definition_list = self.value_definitions
        else:
            definition_list = self.value_group_definitions[group]

        for definition_name in definition_list:
            return_list[definition_name] = self.get_value(definition_name, with_local_name)

        return return_list

    def get_value(self, value_name: str, with_local_name: bool=False):
        """ Get value by name.

        :param with_local_name: if yes output is a tuple with (name, value) instead of value only
        :param value_name: name of the value as specified in address_dict
        """

        if not self.value_definitions[value_name]:
            raise core.ValueNotDefinedError("Address for value: '{0}' not defined in address_dict".format(value_name))

        if not self.command_definitions['get_value']:
            raise core.CommandNotDefinedError("Address for command: 'get_value' not defined in command_dict")

        value_definition = self.value_definitions[value_name]

        # Prepare the frame and get the answer
        command_address = self.command_definitions['get_value']['address']
        value_address = value_definition['address']

        answer_frame = self.connection.send(command_address, value_address)

        value = core.get_integer_from_short(answer_frame.payload)
        value = value / value_definition['factor']

        if with_local_name:
            return_list = (value_definition['local_name'], value)
            return return_list
        else:
            return value

    def test_connection(self):
        """ Tests the connection.

            Tests the connection by sending a random string and reading it back.

            :return: True if connection was successful. False otherwise.
        """

        command_address = self.command_definitions['test_connection']['address']
        random_string = core.get_random_string(15)
        payload = core.get_bytes_from_string(random_string)

        try:
            answer_frame = self.connection.send(command_address, payload)
        except core.CommunicationError as e:
            return False

        return_string = core.get_string_from_bytes(answer_frame.payload)

        if return_string == random_string:
            return True

        return False

    def get_version(self):
        """ Gets the software version from the heater.

        :return: A string containing the version
        """

        command_address = self.command_definitions['get_version_and_date']['address']
        answer_frame = self.connection.send(command_address)

        #first 4bytes are the software version the rest is for the date
        version_bytes = answer_frame.payload[:4]

        #convert into . separated string
        version_string = '.'.join(['{:02x}'.format(i) for i in version_bytes])
        return version_string

    def get_date(self):
        """ Gets the date and time from the heater.

        :return: A datetime object
        """

        command_address = self.command_definitions['get_version_and_date']['address']
        answer_frame = self.connection.send(command_address)

        #first 4bytes are the software version the rest is for the date
        date_bytes = answer_frame.payload[4:]

        #convert into . separated string
        return_date = core.get_date_from_byte(date_bytes)
        return return_date

    def get_errors(self):
        """ Get all errors currently in the error buffer. """

        command_start_address = self.command_definitions['get_error']['address']
        command_next_address = self.command_definitions['get_next_error']['address']

        output = []

        error_frames = self.connection.get_list(command_start_address, command_next_address)

        for frame in error_frames:
            error = core.get_error_from_bytes(frame.payload)
            output.append(error)

        return output

    def get_configuration(self):
        """ Get the active and connected boilers, heating circuits and solar. """

        command_address = self.command_definitions['get_configuration']['address']
        answer_frame = self.connection.send(command_address)

        return_dict = core.get_configuration_from_bytes(answer_frame.payload)

        return return_dict


