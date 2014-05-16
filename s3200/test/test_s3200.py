#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from unittest import TestCase
from s3200 import const
from s3200.obj import S3200
from s3200 import core
import datetime


class TestS3200(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.s = S3200('dummy',
                             value_definitions=const.VALUE_DEFINITIONS)

    def test_get_value(self):  #ok
        t = self.s.get_value('residual_oxygen')
        #print(t)
        self.assertEquals(432.2, t)
        #print(str(t[0]) + ": " + str(t[1]))

    def test_test_connection(self):  #ok
        self.assertTrue(self.s.test_connection())

    def test_get_datetime(self): #ok
        self.assertEquals(datetime.datetime(2010, 11, 21, 18, 31), self.s.get_datetime())

    def test_get_version(self):  #ok '50.04.05.09'
        self.assertEquals('50.04.04.14', self.s.get_version())

    def test_get_errors(self):  #ok
        #print(str(self.s.get_errors()[0]))
        self.assertDictEqual({'is_at_ash_outlet': True,
                             'is_receipted': False,
                             'number': 109,
                             'is_dysfunction': False,
                             'is_ongoing': True,
                             'is_at_environment': False,
                             'datetime': datetime.datetime(2013, 4, 11, 10, 38, 37),
                             'is_warning': True,
                             'text': 'Zündversuch nicht gelungen von Hand Anheizen!',
                             'is_at_heating_boiler': False,
                             'status': 4,
                             'status_name': 'Gone',
                             'status_name_local': 'Gegangen'}, self.s.get_errors()[0])

    def test_get_state(self):  #ok
        self.assertEqual('STÖRUNG', self.s.get_state())

    def test_get_mode(self):  #ok
        self.assertEqual('Übergangsbetr', self.s.get_mode())

    def test_get_menu(self):  #ok
        item = self.s.get_menu()[0]
        self.assertEquals("Proportionalfaktor des Mischerreglers", item["text"])
        self.assertEquals(b'\x00\x53', item["address"])

    def test_get_setting(self):  #ok
        self.assertEquals(84, self.s.get_setting('heating_boiler_should_temperature'))

    def test_get_setting_info(self):  #ok
        #print("test_get_setting_info: " + str(self.s.get_setting_info('heating_boiler_should_temperature')))
        self.assertDictEqual({'comma': 0,
                              'max_value': 90,
                              'address': bytearray(b'\x00\x1c'),
                              'value': 84,
                              'standard': 80,
                              'factor': 2,
                              'min_value': 70,
                              'unit': '°'}, self.s.get_setting_info('heating_boiler_should_temperature'))

    def test_get_configuration(self):  #ok
        #print("test_get_configuration: " + str(self.s.get_configuration()))
        self.assertDictEqual({'boiler_7': False,
                              'boiler_4': False,
                              'boiler_6': False,
                              'boiler_5': False,
                              'solar_2': False,
                              'boiler_2': False,
                              'boiler_3': False,
                              'heater_circuit_1': True,
                              'boiler_8': False,
                              'solar_1': False,
                              'remote_control_2': False,
                              'heater_circuit_2': True,
                              'remote_control_1': False,
                              'boiler_1': True}, self.s.get_configuration())

    def test_get_digital_input(self):  #no
        #print("test_get_digital_input: " + str(self.s.get_digital_input('door_contact')))
        self.assertEquals(True, self.s.get_digital_input('door_contact'))

    def test_get_digital_output(self):  #no
        #print("test_get_digital_output: " + str(self.s.get_digital_output('heating_circuit_pump_1')))
        self.assertEquals(True, self.s.get_digital_output('heating_circuit_pump_1'))

    def test_get_analog_output(self):
        #print("test_get_analog_output: " + str(self.s.get_analog_output('primary_air')))
        self.assertEquals(99, self.s.get_analog_output('primary_air'))

    def test_get_available_values(self):  #ok
        #print("test_get_available_values: " + str(self.s.get_available_values()))
        self.assertDictEqual({'factor': 2,
                              'text': 'Kesseltemperatur',
                              'address': b'\x00\x00',
                              'unit': '°'}, self.s.get_available_values()[0])

    def test_set_setting(self):
        self.assertRaises(core.ReadonlyError, self.s.set_setting, 'heating_boiler_should_temperature', 42)
        self.s = S3200('dummy', readonly=False)

        self.s.set_setting('heating_boiler_should_temperature', 84)  # 84 is already set
        self.s.set_setting('heating_boiler_should_temperature', 81)

        # TODO repair dummy to enable this test
        #self.assertRaises(core.ValueSetError, self.s.set_setting, 'heating_boiler_should_temperature', 120),

        self.s = S3200('dummy', readonly=True)






