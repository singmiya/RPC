#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import grpc

import pi_pb2_grpc
import pi_pb2


def main():
    chanel = grpc.insecure_channel('localhost:8080')
    # 使用Stub
    client = pi_pb2_grpc.PiCalculatorStub(chanel)
    # 调用
    for i in range(100000000000):
        client.Calc(pi_pb2.PiRequest(n=i))
        # print 'pi(%d) = ' % i, client.Calc(pi_pb2.PiRequest(n=i)).value

if __name__ == '__main__':
    main()

    '''
    start: 18-06-23 17:11:51
    end:   18-06-23 17:12:09
    '''