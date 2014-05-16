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
StructDateDayTime = Struct('!7b')
StructDateTime = Struct('!6b')

#### COMMAND AND VALUE DEFINITIONS ####

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
        'description': 'Get the first value from the available values list',
    },
    'get_next_available_value':   {
        'address': b'\x32',
        'description': 'Get the next value from the available values list',
    },
    'get_menu_item':   {
        'address': b'\x37',
        'description': 'Gets the first menu item.',
    },
    'get_next_menu_item':   {
        'address': b'\x38',
        'description': 'Gets the next menu item.',
    },
    'set_setting':   {
        'address': b'\x39',
        'description': 'Set a specific setting',
    },
    'get_configuration':   {
        'address': b'\x40',
        'description': 'Gets the configuration from the heater. eg which boilers are connected',
    },
    'get_version_and_datetime':   {
        'address': b'\x41',
        'description': 'Get Version, Date and Time',
    },
    'get_time_slot':   {
        'address': b'\x42',
        'description': 'Get the first time slot',
    },
    'get_next_time_slot':   {
        'address': b'\x43',
        'description': 'Get the next time slot',
    },
    'get_digital_output':   {
        'address': b'\x44',
        'description': 'Gets the value of a digital (True, False) output.',
    },
    'get_analog_output':   {
        'address': b'\x45',
        'description': 'Gets the value of a analog output (0-100%)',
    },
    'get_digital_input':   {
        'address': b'\x46',
        'description': 'Gets the value of a digital (True, False) output.',
    },
    'get_error':   {
        'address': b'\x47',
        'description': 'Gets the first error from the error list',
    },
    'get_next_error':   {
        'address': b'\x48',
        'description': 'Gets the next error from the error list',
    },
    'set_time_slot':   {
        'address': b'\x50',
        'description': '',
    },
    'get_heater_state_and_mode':   {
        'address': b'\x51',
        'description': 'Gets state and mode from the heater',
    },
    'set_datetime':   {
        'address': b'\x54',
        'description': 'Set the date and time of the heater',
    },
    'get_setting':   {
        'address': b'\x55',
        'description': 'Get the current value and min, max value of the setting',
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

#The address of the settings
SETTING_DEFINITIONS = OrderedDict({
    'heating_boiler_should_temperature':   {'address': b'\x00\x1C', 'factor': 2, 'local_name': 'Kessel-Solltemperatur'},
    'start_firing':   {'address': b'\x02\x52', 'factor': 1, 'local_name': 'Zündung starten'},

})

DIGITAL_INPUT_DEFINITIONS = {
    'door_contact': b'\x00\x00',
    'stb': b'\x00\x01',
    'emergency_off': b'\x00\x01',
    'heating_boiler_release':b'\x00\x1F'
}
DIGITAL_OUTPUT_DEFINITIONS = {
    'heating_circuit_pump_1': b'\x00\x00',
    'heating_circuit_pump_2': b'\x00\x01',
    #...
}
ANALOG_OUTPUT_DEFINITIONS = {
    'primary_air': b'\x00\x00',
    'secondary_air': b'\x00\x01',
    #...
}

TIME_SLOT_DEFINITIONS = {
    'boiler_1_monday': b'\x00',
    'boiler_1_tuesday': b'\x01',
    'boiler_1_wednesday': b'\x02',
    'boiler_1_thursday': b'\x03',
    'boiler_1_friday': b'\x04',
    'boiler_1_saturday': b'\x05',
    'boiler_1_sunday': b'\x06',
}


#### MAPPINGS ####

ERROR_STATE = {
    1: 'New',
    2: 'Quittiert',
    4: 'Gone',
}
ERROR_STATE_LOCAL = {
    1: 'Gekommen',
    2: 'Quittiert',
    4: 'Gegangen',

}
TIME_SLOT_REVERSED = OrderedDict((v, k) for k, v in TIME_SLOT_DEFINITIONS.items())

#### STRUCTURES ####


CONFIGURATION_STRUCTURE = {
    'boiler_1': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 7},
    'boiler_2': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 6},
    'boiler_3': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 5},
    'boiler_4': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 4},
    'boiler_5': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 3},
    'boiler_6': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 2},
    'boiler_7': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 1},
    'boiler_8': {'start': 31, 'end': 32, 'type': 'flag', 'bit': 0},


    'heater_circuit_1': {'start': 37, 'end': 40, 'type': 'flag', 'bit': 23},
    'heater_circuit_2': {'start': 37, 'end': 40, 'type': 'flag', 'bit': 22},

    'remote_control_1': {'start': 45, 'end': 48, 'type': 'flag', 'bit': 23},
    'remote_control_2': {'start': 45, 'end': 48, 'type': 'flag', 'bit': 22},

    'solar_1': {'start': 63, 'end': 64, 'type': 'flag', 'bit': 7},
    'solar_2': {'start': 63, 'end': 64, 'type': 'flag', 'bit': 6},
     # TODO local_name needed???
}
MENU_ITEM_STRUCTURE = {
    'address': {'start': 25, 'end': 27, 'type': 'bytes'},
    'text': {'start': 29, 'end': -1, 'type': 'string'},
}

STATE_AND_MODE_STRUCTURE = {
    'text': {'start': 2, 'end': None, 'type': 'string'},
}

SETTING_STRUCTURE = {
    'address': {'start': 1, 'end': 3, 'type': 'bytes'},
    'unit': {'start': 3, 'end': 4, 'type': 'string'},
    'comma': {'start': 4, 'end': 5, 'type': 'short'},
    'factor': {'start': 6, 'end': 7, 'type': 'short'},
    'value': {'start': 7, 'end': 9, 'type': 'short'},
    'min_value': {'start': 9, 'end': 11, 'type': 'short'},
    'max_value': {'start': 11, 'end': 13, 'type': 'short'},
    'standard': {'start': 13, 'end': 15, 'type': 'short'},
}
DIGITAL_INPUT_STRUCTURE = {
    'mode': {'start': 0, 'end': 1, 'type': 'string'},
    'value': {'start': 1, 'end': 2, 'type': 'short'},
}
DIGITAL_OUTPUT_STRUCTURE = {
    'mode': {'start': 0, 'end': 1, 'type': 'string'},
    'value': {'start': 1, 'end': 2, 'type': 'short'},
}
ANALOG_OUTPUT_STRUCTURE = {
    'mode': {'start': 0, 'end': 1, 'type': 'short'},
    'value': {'start': 1, 'end': 2, 'type': 'short'},
}

TIME_SLOT_STRUCTURE = {
    #'address': {'start': 2, 'end': 3, 'type': 'bytes'},
    'address': {'start': 2, 'end': 3, 'type': 'bytes'},
    'name': {'start': 2, 'end': 3, 'type': 'bytes', 'reference': TIME_SLOT_REVERSED},
    'time_slot_1_start': {'start': 3, 'end': 4, 'type': 'time10'},
    'time_slot_1_end': {'start': 4, 'end': 5, 'type': 'time10'},
    'time_slot_2_start': {'start': 5, 'end': 6, 'type': 'time10'},
    'time_slot_2_end': {'start': 6, 'end': 7, 'type': 'time10'},
    'time_slot_3_start': {'start': 7, 'end': 8, 'type': 'time10'},
    'time_slot_3_end': {'start': 8, 'end': 9, 'type': 'time10'},
    'time_slot_4_start': {'start': 9, 'end': 10, 'type': 'time10'},
    'time_slot_4_end': {'start': 10, 'end': 11, 'type': 'time10'},
}

ERROR_STRUCTURE = {
    'number': {'start': 2, 'end': 3, 'type': 'short'},
    'is_ongoing': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 0},
    'is_at_heating_boiler': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 1},
    'is_at_ash_outlet': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 2},
    'is_at_environment': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 4},
    'is_dysfunction': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 5},
    'is_warning': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 6},
    'is_receipted': {'start': 3, 'end': 4, 'type': 'flag', 'bit': 7},
    'status': {'start': 4, 'end': 5, 'type': 'short'},
    'datetime': {'start': 5, 'end': 11, 'type': 'datetime'},
    'text': {'start': 11, 'end': None, 'type': 'string'},
    'status_name': {'start': 4, 'end': 5, 'type': 'short', 'reference': ERROR_STATE},
    'status_name_local': {'start': 4, 'end': 5, 'type': 'short', 'reference': ERROR_STATE_LOCAL},
}

AVAILABLE_VALUE_STRUCTURE = {
    'factor': {'start': 1, 'end': 3, 'type': 'short'},
    'unit': {'start': 6, 'end': 7, 'type': 'string'},
    'address': {'start': 7, 'end': 9, 'type': 'bytes'},
    'text': {'start': 9, 'end': -1, 'type': 'string'},
}


FORCE_MODE_STRUCTURE = {
    'is_force_active': {'start': 0, 'end': 1, 'type': 'flag', 'bit': 0},
}