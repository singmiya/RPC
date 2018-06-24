# RPC
分布式高并发RPC服务

## 自定义实现
服务端
```
python server.py localhost 8080
```
客户端
```
python client.py
```

## gRPC实现圆周率计算服务

![](https://user-gold-cdn.xitu.io/2018/6/4/163c96b5be229172?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

> **Note**
> 摘自掘金小册《深入理解 RPC : 基于 Python 自建分布式高并发 RPC 服务》@老钱

整个过程分为五步

1. 编写协议文件`pi.proto`
2. 使用`grpc_tools`工具将`pi.proto`编译成`pi_pb2.py`和`pi_pb2_grpc.py`两个文件
3. 使用`pi_pb2_grpc.py`文件中的服务器接口类，编写服务器具体的逻辑实现
4. 使用`pi_pb2_grpc.py`文件中的客户端Stub，编写客户端交互代码
5. 分别运行服务器和客户端，观察输出结果

服务端
```
python server.py localhost 8080
```

客户端
```
1. time python client.py 
2. time python multithread_client.py # 使用线程池调用
```

## Thrift 实现圆周率计算服务
![](https://user-gold-cdn.xitu.io/2018/6/5/163cefafce5878f8?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
> **Note**
> 摘自掘金小册《深入理解 RPC : 基于 Python 自建分布式高并发 RPC 服务》@老钱