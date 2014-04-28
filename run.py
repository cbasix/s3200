#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pydevd
pydevd.settrace('192.168.17.103', port=8880, stdoutToServer=True, stderrToServer=True)
from s3200 import constants
from s3200.obj import S3200

if __name__ == '__main__':

    s = S3200(
              value_definitions=constants.VALUE_DEFINITIONS,
              value_group_definitions=constants.VALUE_GROUP_DEFINITIONS)
    print("T:"+str(s.get_errors()))
