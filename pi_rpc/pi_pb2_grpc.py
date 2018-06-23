# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import pi_pb2


class PiCalculatorStub(object):
    """pi service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.Calc = channel.unary_unary(
            '/pi.PiCalculator/Calc',
            request_serializer=pi_pb2.PiRequest.SerializeToString,
            response_deserializer=pi_pb2.PiResponse.FromString,
        )


class PiCalculatorServicer(object):
    """pi service
    """

    def Calc(self, request, context):
        """pi method
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PiCalculatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Calc': grpc.unary_unary_rpc_method_handler(
            servicer.Calc,
            request_deserializer=pi_pb2.PiRequest.FromString,
            response_serializer=pi_pb2.PiResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'pi.PiCalculator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
