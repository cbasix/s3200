#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#import pydevd
#pydevd.settrace('192.168.17.103', port=8880, stdoutToServer=True, stderrToServer=True)
from s3200 import const
from s3200 import core
from s3200.obj import S3200
from s3200.core import Frame
from s3200.net import Connection


def main():
    s = S3200(readonly=False)
    #print("T:"+str(s.get_errors()))
    # values = s.get_available_values()
    # print(values)
    # for value in values:
    #     print('Text: {0}        +++Address: {1}'.format(value['text'], core.convert_bytes_to_hex(value['address'])))
    # errors = s.get_errors()
    # print(errors)
    # for error in errors:
    #     print('Text: {0}        Status: {1}'.format(error['text'], error['status_name_local']))

    #menu = s.get_menu()
    #for item in menu:
    #    print('Status: {1} Text: {0}'.format(item['text'], core.convert_bytes_to_hex(item['address'])))
    # f = Frame.from_bytes(b'\x02\xFD\x00\x07\x45\x00\x00\x00\x01\x00\x02\x00\xC2')
    # c = Connection()
    # print(str(c.send_frame(f).to_bytes()))

    print('Heizkreis 1 Pumpe:' + str(s.get_digital_output('heating_circuit_pump_1')))
    print('Türe:' + str(s.get_digital_input('door_contact')))
    print('Primärluft:' + str(s.get_analog_output('primary_air')))
    print(s.get_setting_info('heating_boiler_should_temperature'))
    print(s.get_value('boiler_1_temperature'))
    print(s.get_state())
    #s.set_setting('heating_boiler_should_temperature', 80)
    #s.set_setting('heating_boiler_should_temperature', 99)
    #print(s.get_setting_info('heating_boiler_should_temperature'))


if __name__ == '__main__':
    main()