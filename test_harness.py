from concurrent import futures

import grpc

import frr_northbound_pb2_grpc
from frr_northbound_pb2_grpc import NorthboundServicer, NorthboundStub
from frr_northbound_pb2 import GetTransactionRequest, GetTransactionResponse, DataTree, Encoding

# python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. frr-northbound.proto


class FakeNorthboundServicer(NorthboundServicer):

    def GetTransaction(self, request, context):
        data_tree = DataTree(encoding=Encoding.JSON, data="{}")
        return GetTransactionResponse(config=data_tree)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    frr_northbound_pb2_grpc.add_NorthboundServicer_to_server(
        FakeNorthboundServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    return server


if __name__ == '__main__':

    server = serve()

    channel = grpc.insecure_channel('localhost:50051')
    stub = NorthboundStub(channel)

    request = GetTransactionRequest()
    request.transaction_id = 123

    response = stub.GetTransaction(request)
    print("Response: ", response.config.data)

    server.stop(grace=0)
