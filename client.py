# coding: utf-8

import hashlib
import grpc
import chatroom_pb2 as proto
import chatroom_pb2_grpc


class ChatClient(object):
  
    def __init__(self, stub):
        self.stub = stub

    def register(self):
        username = input('Register a new user.\nusername: ')
        password = input('password: ')
        password2 = input('password again: ')
        if password != password2:
            print(input('password doesn\'t match'))
        user = proto.User(username=username, password=hashlib.md5(('%s_%s' % (username, password)).encode('utf8')).hexdigest())
        self.stub.register(user)
        print('Register Successful')
        self.name = username
        
    def login(self):
        print("try to login...please input your information")
        username = input('username: ')
        password = input('password: ')
        self.name = username
        rsp = self.stub.login(proto.User(username=username, password=hashlib.md5(('%s_%s' % (username, password)).encode('utf8')).hexdigest()))
        self.token = rsp.token
        print('login successful and get a token from server')

    def add_friend(self, name):
        request = proto.addFriendRequest(user=self.name, token=self.token, friend=name)
        rsp = self.stub.addFriend(request)
        print('response message %s ' % rsp.msg)

    def list_friends(self):
        request = proto.listFriendsRequest(user=self.name, token=self.token)
        rsp = self.stub.listFriends(request)
        print('check your friends: %s' % rsp.friends)


    def get_new_friends(self):
        request = proto.getNewFriendRequest(user=self.name, token=self.token)
        friends = self.stub.getNewFriend(request)
        for friend in friends:
            print('receive new friend request: %s' % friend)
            request = proto.acceptNewFriendRequest(user=self.name, token=self.token, friend=friend.name)
            self.stub.acceptNewFriend(request)
            print('accept new friend %s' % friend)

    def talk(self):
        def msg_iterator():
            while(True):
                Me = input("Me: ")
                msg = proto.Msg(content=Me)
                yield msg
        for rsp in stub.talk(msg_iterator()):
            print('Server: %s' % rsp.content)



if __name__ == "__main__":
    channel = grpc.insecure_channel("localhost:9123")
    stub = chatroom_pb2_grpc.ChatRoomStub(channel)
    print("stub = ", stub)
    client = ChatClient(stub)
    choose = int(input('Welcome to this shell chatroom\nEnter 1 to register.\nEnter 2 to login.\n'))
    print("choose = ", choose)
    if choose == 1:
        client.register()
    elif choose == 2:
        client.login()
    # client.add_friend("Mike")
    # client.add_friend("Jack")
    # client.list_friends()
    # client.get_new_friends()
    # client.talk(stub)