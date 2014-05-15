#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#import pydevd
#pydevd.settrace('192.168.17.103', port=8880, stdoutToServer=True, stderrToServer=True)
from s3200 import const
from s3200 import core
from s3200.obj import S3200

if __name__ == '__main__':

    s = S3200()
    #print("T:"+str(s.get_errors()))
    # values = s.get_available_values()
    # print(values)
    # for value in values:
    #     print('Text: {0}        +++Address: {1}'.format(value['text'], core.convert_bytes_to_hex(value['address'])))
    # errors = s.get_errors()
    # print(errors)
    # for error in errors:
    #     print('Text: {0}        Status: {1}'.format(error['text'], error['status_name_local']))

    menu = s.get_menu()
    for item in menu:
        print('Status: {1} Text: {0}'.format(item['text'], core.convert_bytes_to_hex(item['address'])))
