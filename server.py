#coding: utf-8

import grpc
from concurrent import futures
import time
import hashlib
import sqlite3

import chatroom_pb2_grpc
import chatroom_pb2 as proto

class Server(chatroom_pb2_grpc.ChatRoomServicer):
    pass
def serve():
    print("Starting Server....")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatroom_pb2_grpc.add_ChatRoomServicer_to_server(Server(),server)
    server.add_insecure_port('[::]:9123')
    server.start()
    print("Server Started...Listen on [9123]")
    try:
        while True:
            time.sleep(60 * 60)
    except KeyboardInterrupt:
        server.stop(0)
if __name__ == "__main__":
    serve()