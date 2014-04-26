#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from collections import OrderedDict
from unittest import TestCase
from s3200.core import CommunicationError
from s3200.net import Connection, Frame
from s3200.test import constants
from s3200.obj import S3200


class TestS3200(TestCase):
    def setUp(self):
        self.s = S3200('dummy',
                       value_definitions=constants.VALUE_DEFINITIONS,
                       value_group_definitions=constants.VALUE_GROUP_DEFINITIONS)

    def test_get_value_list(self):
        t = self.s.get_value_list('boiler_1', with_local_name=True)
        self.assertEquals(t, OrderedDict([('boiler_1_temperature', ('Boilertemperatur 1', 2161.0)),
                                        ('boiler_1_pump', ('Boilerpumpenansteuerung 1', 4322.0))]))
        #print(t)
        #for k, v in t.items():
        #    print(str(v[0]) + ": " + str(v[1]))

    def test_get_value(self):
        t = self.s.get_value('residual_oxygen')
        #print(t)
        self.assertEquals(t, 432.2)
        #print(str(t[0]) + ": " + str(t[1]))

    def test_test_connection(self):
        self.s.test_connection()