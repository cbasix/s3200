#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from datetime import datetime, time
from s3200 import const, core, net
from s3200.net import Frame


class S3200(object):
    """ A class representing a s3200 object. """

    def __init__(self, serial_port_name="/dev/ttyAMA0",
                 readonly=True,
                 value_definitions=const.VALUE_DEFINITIONS,
                 setting_definitions=const.SETTING_DEFINITIONS,
                 command_definitions=const.COMMAND_DEFINITIONS,
                 digital_input_definitions=const.DIGITAL_INPUT_DEFINITIONS,
                 digital_output_definitions=const.DIGITAL_OUTPUT_DEFINITIONS,
                 analog_output_definitions=const.ANALOG_OUTPUT_DEFINITIONS,
                 ):

        self.connection = net.Connection(serial_port_name=serial_port_name)
        self.readonly = readonly
        self.value_definitions = value_definitions
        self.setting_definitions = setting_definitions
        self.command_definitions = command_definitions
        self.digital_input_definitions = digital_input_definitions
        self.digital_output_definitions = digital_output_definitions
        self.analog_output_definitions = analog_output_definitions

    def _test_readonly_(self):
        if self.readonly:
            raise core.ReadonlyError("Can not set values in readonly mode.")

    def get_value(self, *args: str, with_local_name: bool=False):
        """ Get value by name.

        :param with_local_name: if yes output is a tuple with (name, value) instead of value only
        :param args: name of the value as specified in address_dict
        """
        return_list = []
        for value_name in args:
            if not self.value_definitions[value_name]:
                raise core.ValueNotDefinedError("Address for value: '{0}' not defined in address_dict".format(value_name))

            if not self.command_definitions['get_value']:
                raise core.CommandNotDefinedError("Address for command: 'get_value' not defined in command_dict")

            value_definition = self.value_definitions[value_name]

            # Prepare the frame and get the answer
            command_address = self.command_definitions['get_value']['address']
            value_address = value_definition['address']

            answer_frame = self.connection.send(command_address, value_address)

            value = core.convert_short_to_integer(answer_frame.payload)
            value = value / value_definition['factor']

            if with_local_name:
                return_list.append(value_definition['local_name'], value)
            else:
                return_list.append(value)

            if len(args) == 1:
                return return_list[0]
            else:
                return return_list


    def test_connection(self):
        """ Tests the connection.

            Tests the connection by sending a random string and reading it back.

            :return: True if connection was successful. False otherwise.
        """

        command_address = self.command_definitions['test_connection']['address']
        random_string = core.get_random_string(15)
        payload = core.convert_string_to_bytes(random_string)

        try:
            answer_frame = self.connection.send(command_address, payload)
        except core.CommunicationError as e:
            return False

        return_string = core.convert_bytes_to_string(answer_frame.payload)

        if return_string == random_string:
            return True

        return False

    def get_version(self):
        """ Gets the software version from the heater.

        :return: A string containing the version
        """

        command_address = self.command_definitions['get_version_and_datetime']['address']
        answer_frame = self.connection.send(command_address)

        #first 4bytes are the software version the rest is for the date
        version_bytes = answer_frame.payload[:4]

        #convert into . separated string
        version_string = '.'.join(['{:02x}'.format(i) for i in version_bytes])
        return version_string

    def get_datetime(self):
        """ Gets the date and time from the heater.

        :return: A datetime object
        """

        command_address = self.command_definitions['get_version_and_datetime']['address']
        answer_frame = self.connection.send(command_address)

        #first 4bytes are the software version the rest is for the date
        date_bytes = answer_frame.payload[4:]

        #convert into . separated string
        return_date = core.convert_bytes_to_datedaytime(date_bytes)
        return return_date

    def set_datetime(self, datetime_to_set: datetime):
        """ Set the date and time of the heater. """
        self._test_readonly_()

        date_bytes = core.get_bytes_from_date_day_time(datetime_to_set)

        command_address = self.command_definitions['set_datetime']['address']
        payload = date_bytes
        answer_frame = self.connection.send(command_address, payload)

        # TODO Test answer frame

    def get_errors(self):
        """ Get all errors currently in the error buffer. """

        command_start_address = self.command_definitions['get_error']['address']
        command_next_address = self.command_definitions['get_next_error']['address']

        output = []

        error_frames = self.connection.get_list(command_start_address, command_next_address)

        for frame in error_frames:
            error = core.convert_bytes_to_error(frame.payload)
            output.append(error)

        return output

    def get_time_slots(self):

        command_start_address = self.command_definitions['get_time_slot']['address']
        command_next_address = self.command_definitions['get_next_time_slot']['address']

        output = []

        time_slots = self.connection.get_list(command_start_address, command_next_address)

        for frame in time_slots:
            time_slot = core.convert_structure_to_dict(frame.payload, const.TIME_SLOT_STRUCTURE)

            output.append(time_slot)

        return output

    def set_time_slot(self,
                      item: str,
                      weekday: int,
                      time_slot_1_start: time,
                      time_slot_1_end: time,
                      time_slot_2_start: time,
                      time_slot_2_end: time,
                      time_slot_3_start: time,
                      time_slot_3_end: time,
                      time_slot_4_start: time,
                      time_slot_4_end: time,
                      ):
        self._test_readonly_()
        raise NotImplementedError()

        data_bytes = core.convert_time_slot_to_bytes(item,
                                                   weekday,
                                                   time_slot_1_start,
                                                   time_slot_1_end,
                                                   time_slot_2_start,
                                                   time_slot_2_end,
                                                   time_slot_3_start,
                                                   time_slot_3_end,
                                                   time_slot_4_start,
                                                   time_slot_4_end,)

        command_address = self.command_definitions['set_time_slot']['address']
        frame = Frame(command_address, data_bytes)
        answer_frame = self.connection.send_frame(frame)

        # TODO Check answer frame
        #if not answer_frame == frame:
        #    raise core.ValueSetError('Error occurred while setting value.')

    def get_configuration(self):
        """ Get the active and connected boilers, heating circuits and solar. """

        command_address = self.command_definitions['get_configuration']['address']
        answer_frame = self.connection.send(command_address)

        return_dict = core.convert_bytes_to_configuration(answer_frame.payload)

        return return_dict

    def get_state(self):
        """ Get the state of the heater.

         Example: Heizen(Heating) """

        command_address = self.command_definitions['get_heater_state_and_mode']['address']
        answer_frame = self.connection.send(command_address)

        state = core.convert_bytes_to_state(answer_frame.payload)

        return state

    # TODO better docstrings
    def get_mode(self):
        """ Get the mode of the heater.

         Example: Übergangsbetr """
        command_address = self.command_definitions['get_heater_state_and_mode']['address']
        answer_frame = self.connection.send(command_address)

        mode = core.convert_bytes_to_mode(answer_frame.payload)

        return mode

    def get_menu(self):

        command_start_address = self.command_definitions['get_menu_item']['address']
        command_next_address = self.command_definitions['get_next_menu_item']['address']

        output = []

        error_frames = self.connection.get_list(command_start_address, command_next_address)

        for frame in error_frames:
            error = core.convert_bytes_to_menu_item(frame.payload)
            output.append(error)

        return output

    def get_available_values(self):

        command_start_address = self.command_definitions['get_available_value']['address']
        command_next_address = self.command_definitions['get_next_available_value']['address']

        output = []

        available_value_frames = self.connection.get_list(command_start_address, command_next_address)

        for frame in available_value_frames:
            available_value = core.convert_structure_to_dict(frame.payload, const.AVAILABLE_VALUE_STRUCTURE)
            output.append(available_value)

        return output

    def get_setting(self, setting_name):

        command_address = self.command_definitions['get_setting']['address']
        value_address = self.setting_definitions[setting_name]['address']

        answer_frame = self.connection.send(command_address, value_address)

        setting = core.convert_bytes_to_setting(answer_frame.payload)

        return_value = setting['value'] / setting['factor']

        if setting['comma'] == 0:
            return_value = int(return_value)

        return return_value

    def get_setting_info(self, setting_name):

        command_address = self.command_definitions['get_setting']['address']
        value_address = self.setting_definitions[setting_name]['address']

        answer_frame = self.connection.send(command_address, value_address)

        setting = core.convert_bytes_to_setting(answer_frame.payload)

        setting['value'] = setting['value'] / setting['factor']

        if setting['comma'] == 0:
            setting['value'] = int(setting['value'])

        return setting

    def set_setting(self, setting_name, value):
        self._test_readonly()
        raise NotImplementedError()

    def get_digital_input(self, input_name):

        command_address = self.command_definitions['get_digital_input']['address']
        value_address = self.digital_input_definitions[input_name]

        answer_frame = self.connection.send(command_address, value_address)

        digital_input = core.convert_structure_to_dict(answer_frame.payload, const.DIGITAL_INPUT_STRUCTURE)

        if digital_input['mode'] == 'A':  # \x41 = A = Auto
            return_bool = bool(digital_input['value'] == 1)
        elif digital_input['mode'] == '0':  # \x30 = 0 = False
            return_bool = False
        elif digital_input['mode'] == '1':  # \x31 = 1 = True
            return_bool = True

        return return_bool

    def get_digital_output(self, output_name):

        command_address = self.command_definitions['get_digital_output']['address']
        value_address = self.digital_output_definitions[output_name]

        answer_frame = self.connection.send(command_address, value_address)

        digital_output = core.convert_structure_to_dict(answer_frame.payload, const.DIGITAL_OUTPUT_STRUCTURE)

        if digital_output['mode'] == 'A':  # \x41 = A = Auto
            return bool(digital_output['value'] == 1)
        elif digital_output['mode'] == '0':  # \x30 = 0 = False
            return False
        elif digital_output['mode'] == '1':  # \x31 = 1 = True
            return True

        return None

    def get_analog_output(self, output_name):
        command_address = self.command_definitions['get_analog_output']['address']
        value_address = self.analog_output_definitions[output_name]

        answer_frame = self.connection.send(command_address, value_address)

        analog_output = core.convert_structure_to_dict(answer_frame.payload, const.ANALOG_OUTPUT_STRUCTURE)

        if analog_output['mode'] == 255:  # Auto mode
            return analog_output['value']
        else:
            return analog_output['mode']  # Manual override

    def set_force_mode(self, is_force_mode: bool):
        """ Sets the Force mode.

        Force mode is a testing mode. When force mode is active you can override the input and output values
        of the heater manually.  If the heater receives no command within 30 seconds the force mode gets
        deactivated automatically.
        """

        self._readonly_test()
        raise NotImplementedError()

        # TODO implement enter force mode

    def get_force_mode(self):
        raise NotImplementedError()

        # TODO implement get force mode

    def set_digital_input(self, input_name, value):
        if not self.readonly:
            raise NotImplementedError()

    def set_digital_output(self, output_name, value):
        if not self.readonly:
            raise NotImplementedError()

    def set_analog_output(self, output_name, value):
        if not self.readonly:
            raise NotImplementedError()

    # TODO implement force set methods