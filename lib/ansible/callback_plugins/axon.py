#!/usr/bin/env python
# coding:utf-8

import os
try:
    import json
except ImportError:
    import simplejson as json
import struct
import socket
import time

    
class AxonClient(object):
    def __init__(self, addr, timeout=10):
        self._addr = addr
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(addr)
        self._sock = sock

        self.head_patt = struct.Struct('>I')

    def push(self, *args):
        if(len(args)>1):
            chunks = []
            for arg in args:
                chunks.append(self.serialize(arg))
            self.send(self.serialize(''.join(chunks), meta=0))
        else:
            self.send(self.serialize(args[0]))

    def send(self, msg):
        self._sock.send(msg)

    def serialize(self, msg, meta=2):
        # if not isinstance(msg, basestring):
        msg = json.dumps(msg)
        return self.head_patt.pack(len(msg)|meta<<24)+msg

if __name__=='__main__':
    client = AxonClient(('127.0.0.1', 3055))
    client.push(1, 'b')
