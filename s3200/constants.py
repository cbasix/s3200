#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from struct import Struct
from collections import OrderedDict

#---STATIC VARIABLES---
START_BYTES = b'\x02\xFD'

#List of bytes to escape. Reverse key and value, to get unescape list
ESCAPE_LIST = OrderedDict(
    [
        (b'\x2B', b'\x2B\x00'),
        (b'\xFE', b'\xFE\x00'),
        (b'\x02', b'\x02\x00'),
        (b'\x11', b'\xFE\x12'),
        (b'\x13', b'\xFE\x14'),
    ]
)
UNESCAPE_LIST = OrderedDict((v, k) for k, v in ESCAPE_LIST.items())

#The bytes which identify that something is escaped
ESCAPED_IDENTIFIER = bytes([0x02, 0xFE, 0x2B])

#Structs
StructShort = Struct('!h')
StructDate = Struct('!7b')

#The address of the actual values
VALUE_DEFINITIONS = OrderedDict({
    'heating_boiler_temperature':   {'address': b'\x00\x00', 'factor': 2, 'local_name': 'Heizkesseltemperatur'},
    'exhaust_temperature':          {'address': b'\x00\x01', 'factor': 1, 'local_name': 'Abgastemperatur'},
    'board_temperature':            {'address': b'\x00\x02', 'factor': 2, 'local_name': 'Boardtemperatur'},
    'residual_oxygen':              {'address': b'\x00\x03', 'factor': 10, 'local_name': 'Restsauerstoff'},
    'outside_temperature':          {'address': b'\x00\x04', 'factor': 2, 'local_name': 'Außentemperatur'},
    'primary_air_inlet_position':   {'address': b'\x00\x05', 'factor': 1, 'local_name': 'Primärluftposition'},
    'secondary_air_inlet_position': {'address': b'\x00\x06', 'factor': 1, 'local_name': 'Sekundärluftposition'},
    'air_fan_rotation_speed':       {'address': b'\x00\x07', 'factor': 1, 'local_name': 'Saugzugdrehzahl'},

    'heater_circuit_1_is_temperature':      {'address': b'\x00\x15', 'factor': 2, 'local_name': 'Heizkreis 1 Ist'},
    'heater_circuit_1_should_temperature':  {'address': b'\x00\x16', 'factor': 2, 'local_name': 'Heizkreis 1 Soll'},

    'boiler_1_temperature':              {'address': b'\x00\x5d', 'factor': 2, 'local_name': 'Boilertemperatur 1'},
    'operating_hours':                   {'address': b'\x00\x62', 'factor': 1, 'local_name': 'Betriebsstunden'},
    'operating_hours_fire_preservation': {
        'address': b'\x00\x73',
        'factor': 1,
        'local_name': 'Betriebsstunden Feuererhaltung'
    },

    'buffer_1_top_temperature':     {'address': b'\x00\x76', 'factor': 2, 'local_name': 'Puffer 1 oben'},
    'buffer_1_middle_temperature':  {'address': b'\x00\x77', 'factor': 2, 'local_name': 'Puffer 1 mitte'},
    'buffer_1_bottom_temperature':  {'address': b'\x00\x78', 'factor': 2, 'local_name': 'Puffer 1 unten'},

    'buffer_1_pump':    {'address': b'\x00\x8c', 'factor': 1, 'local_name': 'Pufferpumpenansteuerung 1'},
    'boiler_1_pump':    {'address': b'\x00\x90', 'factor': 1, 'local_name': 'Boilerpumpenansteuerung 1'},
})

VALUE_GROUP_DEFINITIONS = OrderedDict({
    'important': [
        'heating_boiler_temperature',
        'outside_temperature',
        'boiler_1_temperature',
        'buffer_1_top_temperature',
        'buffer_1_middle_temperature',
        'buffer_1_bottom_temperature',
    ],
    'heater': [
        'heating_boiler_temperature',
        'exhaust_temperature',
        'board_temperature',
        'residual_oxygen',
        'outside_temperature',
        'primary_air_inlet_position',
        'secondary_air_inlet_position',
        'air_fan_rotation_speed',
        'heater_circuit_1_is_temperature',
        'heater_circuit_1_should_temperature',
        'operating_hours',
        'operating_hours_fire_preservation',
    ],
    'boiler_1': [
        'boiler_1_temperature',
        'boiler_1_pump'
    ],
    'buffer_1': [
        'buffer_1_top_temperature',
        'buffer_1_middle_temperature',
        'buffer_1_bottom_temperature',
        'buffer_1_pump',
    ],

})

COMMAND_DEFINITIONS = {
    'test_connection':   {
        'address': b'\x22',
        'description': 'Returns the given frame. For testing the connection',
    },
    'get_value':   {
        'address': b'\x30',
        'description': 'Read a value from the heater.',
    },
    'get_available_value':   {
        'address': b'\x31',
        'description': '',
    },
    'get_next_available_value':   {
        'address': b'\x32',
        'description': '',
    },
    'get_menu_item':   {
        'address': b'\x37',
        'description': '',
    },
    'get_next_menu_item':   {
        'address': b'\x38',
        'description': '',
    },
    'set_setting':   {
        'address': b'\x39',
        'description': '',
    },
    'get_configuration':   {
        'address': b'\x40',
        'description': '',
    },
    'get_version_and_date':   {
        'address': b'\x41',
        'description': 'Get Version, Date and Time',
    },
    'get_time_slot':   {
        'address': b'\x42',
        'description': '',
    },
    'get_next_time_slot':   {
        'address': b'\x43',
        'description': '',
    },
    'get_digital_output':   {
        'address': b'\x44',
        'description': '',
    },
    'get_analog_output':   {
        'address': b'\x45',
        'description': '',
    },
    'get_digital_input':   {
        'address': b'\x46',
        'description': '',
    },
    'get_error':   {
        'address': b'\x47',
        'description': '',
    },
    'get_next_error':   {
        'address': b'\x48',
        'description': '',
    },
    'set_time_slot':   {
        'address': b'\x50',
        'description': '',
    },
    'get_heater_state':   {
        'address': b'\x51',
        'description': '',
    },
    'set_date':   {
        'address': b'\x54',
        'description': '',
    },
    'get_setting':   {
        'address': b'\x55',
        'description': '',
    },
    'manipulate_digital_output':   {
        'address': b'\x58',
        'description': '',
    },
    'manipulate_analog_output':   {
        'address': b'\x59',
        'description': '',
    },
    'manipulate_digital_input':   {
        'address': b'\x5A',
        'description': '',
    },
    'get_force':   {
        'address': b'\x5E',
        'description': '',
    },
    'set_force':   {
        'address': b'\x7E',
        'description': '',
    },

}

ERROR_DEFINITION = {
    #maybe the error number is 3 instead of 1 byte ... so start 0 is maybe right
    'number': {'start': 2, 'end': 3},
    'info_byte': {'start': 3, 'end': 4},
    'status': {'start': 4, 'end': 5},
    'datetime': {'start': 5, 'end': 12},
    'text': {'start': 12, 'end': -1},
}

INFO_BYTE_DEFINITION = {
    'is_ongoing': 0,
    'is_at_heating_boiler': 1,
    'is_at_ash_outlet': 2,
    'is_at_environment': 3,
    'is_dysfunction': 5,
    'is_warning': 6,
    'is_receipted': 7,
}