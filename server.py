#coding: utf-8

import grpc
from concurrent import futures
import time
import hashlib
import sqlite3

import chatroom_pb2_grpc
import chatroom_pb2 as proto

class Server(chatroom_pb2_grpc.ChatRoomServicer):
    def __init__(self):
        self.tokens = {}
        self.friends = {}
        self.friend_req = {}
        self.conn = sqlite3.connect('chatroom.db', check_same_thread=False)
        self.c = self.conn.cursor()

    def register(self, request, context):
        username = request.username
        password = request.password
        try:
            self.c.execute("insert into users(username, password) values('%s', '%s')" % (username, password))
        except Exception as ex:
            print('user %s register failed: %s' % (username, ex))
            return proto.SimpleResponse(msg='register failed: %s' % ex, state=proto.Fail)
        else:
            print('user %s register successful' % username)
            return proto.SimpleResponse(msg='register successful', state=proto.Success)
    
    def login(self, request, context):
        username = request.username
        password = request.password
        stored_pwd = self.c.execute("select password from users where username='%s'" % username)
        if password != stored_pwd:
            return proto.SimpleResponse(msg="unmatch username and password", state=proto.Fail)
        print('user %s login' % username)
        token = hashlib.md5('%s_%s'% (time.ctime(), username)).hexdigest()
        self.tokens[username] = token
        return proto.LoginResponse(token=token, state=proto.Success)

    def addFriend(self, request, context):
        user = request.user
        token = request.token
        friend = request.friend
        if self.tokens.get(user) == token and token is not None:
            print('user %s trying to add %s as friend' % (user, friend))
            self.friend_req.setdefault(user, [])
            self.friend_req[user].append(friend)
        return proto.SimpleResponse(msg='your request to add %s as your friend has been sent.' % friend, state=proto.Success)


    def listFriends(self, request, context):
        token = request.token
        user = request.user
        rsp = proto.listFriendsResponse()
        if self.tokens.get(user) == token and token is not None and self.friends.get(user) is not None:
            for friend in self.friends.get(user):
                f = rsp.friends.add()
                f.name = friend
        return rsp


    def getNewFriend(self, request, context):
        user = request.user
        token = request.token
        for friend in self.friend_req[user]:
            yield proto.Friend(name=friend)


    def acceptNewFriend(self, request, context):
        user = request.user
        friend = request.friend
        token = request.token
        if friend in self.friend_req[user] and self.tokens.get(user) == token and token is not None:
            self.friends.setdefault(user, [])
            self.friends[user].append(friend)
            print('user %s accepted to add %s as friend' % (user, friend))
        return proto.SimpleResponse(msg='your have acceopted to add %s as your friend.' % friend, state=proto.Success)


    def talk(self, request_iterator, context):
        for msg in request_iterator:
            print('Client: %s' % msg.content)
            input = raw_input('Me: ')
            yield proto.Msg(content=input)

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