#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import math

import grpc
import time
from concurrent import futures

import pi_pb2_grpc
import pi_pb2


class PiCalculatorServicer(pi_pb2_grpc.PiCalculatorServicer):
    def Calc(self, request_iterator, context):
        # request是一个迭代器参数，对应一个stream请求
        for request in request_iterator:
            # if request.n < 0:
            #     context.set_code(grpc.StatusCode.INVALID_ARGUMENT) # 参数错误
            #     context.set_details('request number should be positive') # 错误具体说明
            #     yield pi_pb2.PiResponse()
            # 50% 的概率会有响应
            # if random.randint(0, 1) == 1:
            #     continue
            s = 0.0
            for i in range(request.n):
                s += 1.0 / (2 * i + 1) / (2 * i + 1)
                # 响应是一个生成器，一个响应对应一个请求
                context.set_code(grpc.StatusCode.OK)
                yield pi_pb2.PiResponse(n=i, value=math.sqrt(8 * s))


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = PiCalculatorServicer()
    pi_pb2_grpc.add_PiCalculatorServicer_to_server(servicer, server)
    server.add_insecure_port('localhost:8080')
    server.start()
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()
