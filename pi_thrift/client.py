#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from thrift.protocol import TCompactProtocol
from thrift.transport import TSocket, TTransport

from pi.PiService import Client, PiRequest, IllegalArgument

if __name__ == '__main__':
    sock = TSocket.TSocket('127.0.0.1', 8080)
    transport = TTransport.TBufferedTransport(sock) # 缓冲模式
    protocol = TCompactProtocol.TCompactProtocol(transport) # 紧凑模式
    client = Client(protocol)

    transport.open() # 开启连接
    for i in range(100000000000):
        try:
            res = client.calc(PiRequest(n=i))
            # print 'pi(%d)' % i, res.value
        except IllegalArgument as ia:
            print 'pi(%d)' % i, ia.message
    transport.close()