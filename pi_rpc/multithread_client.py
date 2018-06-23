#!/usr/bin/python
# -*- coding: utf-8 -*-
import grpc
from concurrent import futures

import pi_pb2, pi_pb2_grpc


def pi(client, k):
    return client.Calc(pi_pb2.PiRequest(n=k)).value


def main():
    channel = grpc.insecure_channel('localhost:8080')
    # client 对象是线程安全的
    client = pi_pb2_grpc.PiCalculatorStub(channel)
    # 客户端使用线程池执行
    pool = futures.ThreadPoolExecutor(max_workers=4)
    results = []
    for i in range(1000):
        results.append((i, pool.submit(pi, client, i)))
    # 等待所有任务执行完毕
    pool.shutdown()
    # for i, future in results:
    #     print i, future.result()


if __name__ == '__main__':
    main()
