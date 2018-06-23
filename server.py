#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncore
import json
import os
import signal
import struct
import traceback
import socket
import sys

import errno

from cStringIO import StringIO

import math
from kazoo.client import KazooClient


class RPCHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.addr = addr
        self.handlers = {
            "ping": self.ping,
            "pi": self.pi
        }
        self.rbuf = StringIO()

    def handle_connect(self):
        print self.addr, 'comes'

    def handle_close(self):
        print self.addr, 'bye'
        self.close()

    def handle_read(self):
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(content)
            if len(content) < 1024:
                break
        self.handle_rpc()

    def handle_rpc(self):
        while True:
            self.rbuf.seek(0) # 把游标设为其缓冲起始处开始读取数据
            length_prefix = self.rbuf.read(4) # 读取内容数据长度
            if len(length_prefix) < 4:
                break
            length, = struct.unpack('I', length_prefix)
            body = self.rbuf.read(length)
            if len(body) < length:
                # 消息不完整
                break
            request = json.loads(body)
            in_ = request['in']
            params = request['params']
            print os.getpid(), in_, params
            handler = self.handlers[in_]
            handler(params)
            left = self.rbuf.getvalue()[length + 4:] # 获取缓冲区剩余的数据
            self.rbuf = StringIO()
            self.rbuf.write(left)
        self.rbuf.seek(0, 2) # 改变游标让后续写入的数据添加到缓冲区末尾

    def ping(self, params):
        self.send_result('pong', params)

    def pi(self, n):
        '''计算圆周率'''
        s = 0.0
        for i in range(n + 1):
            s += 1.0 / math.pow(2 * i + 1, 2)
        result = math.sqrt(8 * s)
        self.send_result('pi_r', result)

    def send_result(self, out, result):
        response = {'out': out, 'result': result}
        body = json.dumps(response)
        length_prefix = struct.pack('I', len(body))
        self.send(length_prefix)
        self.send(body)


class RPCServer(asyncore.dispatcher):
    zk_root = '/demo'
    zk_rpc = zk_root + '/rpc'

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        self.child_pids = []
        if self.prefork(10):
            self.register_zk()
            self.register_parent_signal()
        else:
            self.register_child_signal()

    def prefork(self, n):
        for i in range(n):
            pid = os.fork()
            if pid < 0:  # fork 出错
                raise
            if pid > 0:  # 父进程
                self.child_pids.append(pid)
                continue
            if pid == 0:  # 子进程
                return False
        return True

    def register_zk(self):
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()
        self.zk.ensure_path(self.zk_root)  # 创建根节点
        value = json.dumps({'host': self.host, 'port': self.port})
        # 创建服务子节点
        self.zk.create(self.zk_rpc, value, ephemeral=True, sequence=True)

    def exit_parent(self, sig, frame):
        self.zk.stop()  # 关闭 zk 客户端
        self.close()  # 关闭 serversocket
        asyncore.close_all()  # 关闭所有 clientsocket
        pids = []
        for pid in self.child_pids:
            print 'before kill'
            try:
                os.kill(pid, signal.SIGINT)  # 关闭子进程
                pids.append(pid)
            except OSError, ex:
                if ex.args[0] == errno.ECHILD:  # 目标子进程已经提前挂了
                    continue
                raise
            print 'after kill', pid

        for pid in pids:
            while True:
                try:
                    os.waitpid(pid, 0)  # 收割目标子进程
                    break
                except OSError, ex:
                    if ex.args[0] == errno.ECHILD:  # 子进程已经收割过了
                        break
                    if ex.args[0] != errno.EINTR:
                        raise ex  # 被其他信号打断，需要重试

            print 'wait over', pid

    def reap_child(self, sig, frame):
        print 'before reap'
        while True:
            try:
                info = os.waitpid(-1, os.WNOHANG)  # 收割任意子进程
                break
            except OSError, ex:
                if ex.args[0] == errno.ECHILD:
                    return  # 没有子进程可以收割
                if ex.args[0] != errno.EINTR:
                    raise ex  # 被其他信号打断需要重试
        pid = info[0]
        try:
            self.child_pids.remove(pid)
        except ValueError:
            pass
        print 'after reap', pid

    def register_parent_signal(self):
        signal.signal(signal.SIGINT, self.exit_parent)
        signal.signal(signal.SIGTERM, self.exit_parent)
        signal.signal(signal.SIGCHLD, self.reap_child)  # 监听子进程退出

    def exit_child(self, sig, frame):
        self.close()  # 关闭 serversocket
        asyncore.close_all()  # 关闭所有clientsocket
        print 'all closed'

    def register_child_signal(self):
        signal.signal(signal.SIGINT, self.exit_child)
        signal.signal(signal.SIGTERM, self.exit_child)

    def handle_accept(self):
        pair = self.accept()  # 接收新连接
        if pair is not None:
            print pair
            try:
                sock, addr = pair
                RPCHandler(sock, addr)
            except Exception as e:
                print "xxx>>>>>>>>>>"
                msg = traceback.format_exc()  # 方式1
                print (msg)


if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    RPCServer(host, port)
    asyncore.loop()