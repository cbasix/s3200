#!/usr/bin/python3
# -*- coding: UTF-8 -*-

""" A simplified constants.py for testing

"""

from collections import OrderedDict

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








