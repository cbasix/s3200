#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from unittest import TestCase
from s3200.core import CommunicationError
from s3200.net import Frame, Connection


class TestConnection(TestCase):

    def setUp(self):
        self.c = Connection('dummy')

    def test_send_request(self):

        # Send normal request working hours
        f = Frame(b'\x30', b'\x00\x62')
        return_frame = self.c.send_frame(f)

        self.assertEquals(return_frame.command, b'\x30')
        self.assertEquals(return_frame.payload, b'\x00\x37')

        # Test what does happen when a wrong checksum error occurs
        f = Frame(b'\x30', b'\x00\x59')
        # print('Send:'+str(f))
        # print('Should be:'+str(Frame.from_bytes(b'\x02\xfd\x00\x02\x000\x10h')))
        # return_value = c.send_request(f)
        # print('Is:'+return_value)

        self.assertRaises(CommunicationError, self.c.send_frame, f)
