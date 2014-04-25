#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from collections import OrderedDict
from s3200 import core
from s3200.obj import S3200
from s3200.net import Frame, Connection


if __name__ == '__main__':
    # Frame(b'\x30',b'\x00\x11').toBytes()
    # f = Frame.from_bytes(bytearray.fromhex('02 fd 00 03 30 00 30 04'))
    # print(f)
    # f = Frame(b'\x30',b'\x00\x62')
    # print('Frame print:'+str(f))
    # print('Frame bytearray:'+str(f.toBytes()))
    # print('Frame byte hex:'+convertToHexStr(f.toBytes()))
    # conn = Connection()
    s = S3200('dummy')

    t = s.get_value('residual_oxygen')
    #print(t)
    assert(t == 432.2)
    #print(str(t[0]) + ": " + str(t[1]))

    t = s.get_value_list('boiler_1', with_local_name=True)
    assert(t == OrderedDict([('boiler_1_temperature', ('Boilertemperatur 1', 2161.0)), ('boiler_1_pump', ('Boilerpumpenansteuerung 1', 4322.0))]))
    #print(t)
    #for k, v in t.items():
    #    print(str(v[0]) + ": " + str(v[1]))

    t = s.get_value('operating_hours', with_local_name=True)
    assert(t[1] == 55)
    #print(str(t[0]) + ": " + str(t[1]))

    c = Connection('dummy')
    f = Frame(b'\x30', b'\x00\x59')
    print('Send:'+str(f))
    print('Should be:'+str(Frame.from_bytes(b'\x02\xfd\x00\x02\x000\x10h')))
    print('Is:'+c.send_request(str(f)))








