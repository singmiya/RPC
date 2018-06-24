#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math

from thrift.protocol import TCompactProtocol
from thrift.server import TServer
from thrift.transport import TSocket

from pi.PiService import Iface, Processor, TTransport
from pi.ttypes import PiResponse, IllegalArgument


class PiHandler(Iface):
    def calc(self, req):
        if req.n < 0:
            raise IllegalArgument(message='parameter must be positive')
        s = 0.0
        for i in range(req.n):
            s += 1.0 / (2 * i + 1) / (2 * i + 1)

        return PiResponse(value=math.sqrt(8 * s))

if __name__ == '__main__':
    handler = PiHandler()
    processor = Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=8080)
    tfactory = TTransport.TBufferedTransportFactory() # 缓冲模式
    pfactory = TCompactProtocol.TCompactProtocolFactory() # 紧凑模式

    # 线程池服务RPC请求
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    # 设置线程池数量
    server.setNumThreads(10)
    # 设置线程为daemon，当进程只剩下daemon线程时会立即退出
    server.daemon = True

    # 启动服务
    server.serve()