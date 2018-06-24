#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

import grpc
import time

import sys
from concurrent import futures
import pi_pb2, pi_pb2_grpc


class PiCalculatorServicer(pi_pb2_grpc.PiCalculatorServicer):

    def Calc(self, request, context):
        """计算圆周率的逻辑
        """
        time.sleep(0.01)
        s = 0.0
        for i in range(request.n):
            s += 1.0 / (2 * i + 1) / (2 * i + 1)
        return pi_pb2.PiResponse(value=math.sqrt(8 * s))


def main(addr):
    # 多线程服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 实例化圆周率服务类
    servicer = PiCalculatorServicer()
    # 注册本地服务
    pi_pb2_grpc.add_PiCalculatorServicer_to_server(servicer, server)
    # 监听端口
    server.add_insecure_port(addr)
    # 开始接收请求进行服务
    server.start()
    # 使用ctrl + c 可以退出服务
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise '缺失：host或者port；eg. python server.py 127.0.0.1 8080'
    host = sys.argv[1]
    port = sys.argv[2]

    main(host + ':' + port)
