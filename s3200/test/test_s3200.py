#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from collections import OrderedDict
from unittest import TestCase
from s3200.test import constants
from s3200.obj import S3200
import datetime


class TestS3200(TestCase):
    def setUp(self):
        self.s = S3200('dummy',
                       value_definitions=constants.VALUE_DEFINITIONS,
                       value_group_definitions=constants.VALUE_GROUP_DEFINITIONS)

    def test_get_value_list(self):
        t = self.s.get_value_list('boiler_1', with_local_name=True)
        self.assertEquals(OrderedDict([('boiler_1_temperature', ('Boilertemperatur 1', 2161.0)),
                                        ('boiler_1_pump', ('Boilerpumpenansteuerung 1', 4322.0))]), t)
        #print(t)
        #for k, v in t.items():
        #    print(str(v[0]) + ": " + str(v[1]))

    def test_get_value(self):
        t = self.s.get_value('residual_oxygen')
        #print(t)
        self.assertEquals( 432.2, t)
        #print(str(t[0]) + ": " + str(t[1]))

    def test_test_connection(self):
        self.assertTrue(self.s.test_connection())

    def test_get_date(self):
        self.assertEquals(datetime.datetime(2010, 11, 21, 18, 31), self.s.get_date())

    def test_get_version(self):
        self.assertEquals('50.04.04.14', self.s.get_version())

    def test_get_errors(self):
        self.assertEquals([{'is_at_ash_outlet': False,
                            'is_receipted': True,
                            'number': 109,
                            'is_dysfunction': False,
                            'is_ongoing': False,
                            'is_at_environment': True,
                            'datetime': datetime.datetime(2012, 2, 4, 12, 17, 2),
                            'is_warning': False,
                            'text': 'Zündversuch nicht gelungen von Hand Anheizen!',
                            'status_local_name': 'Gekommen',
                            'is_at_heating_boiler': True,
                            'status_name': 'New',
                            'status': 1}], self.s.get_errors())

    def test_get_state(self):
        self.assertEqual('STÖRUNG', self.s.get_state())

    def test_get_mode(self):
        self.assertEqual('Übergangsbetr', self.s.get_mode())




