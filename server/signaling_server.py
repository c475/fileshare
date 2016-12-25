import os
import sys
import json
import uuid
from pprint import pprint

sys.path.append('/srv/')
sys.path.append('/srv/server/')
sys.path.append('/srv/fileshare/')
sys.path.append('/srv/client/')

from django.conf import settings
from django import setup

settings.configure()
setup()

from twisted.python import log
from twisted.internet import (
    reactor,
    ssl,
    task
)

from autobahn.twisted.websocket import (
    WebSocketServerProtocol,
    WebSocketServerFactory
)


DEBUG = True


class Peers(object):

    def __init__(self):
        self.peers = {}

    def add(self, sid, sock):
        self.peers[sid] = sock

    def remove(self, sid):
        if sid in self.peers:
            del self.peers[sid]

    def subscribe(self, sid, what):
        pass

    def unsubscribe(self, sid, what):
        pass

    def broadcast(self, payload):
        for peer in self.peers:
            self.peers[peer].sendMessage(json.dumps(payload))

    def push(self, payload, to):
        if to in self.peers:
            self.peers[to].sendMessage(json.dumps(payload))

    def getPeers(self, who=None):
        ret = self.peers.keys()
        if who is not None:
            ret.remove(who)
        return ret


class SocketServerFactory(WebSocketServerFactory):

    def __init__(self, *args, **kwargs):
        WebSocketServerFactory.__init__(self, *args, **kwargs)
        self.peers = Peers()

        if DEBUG is True:
            l = task.LoopingCall(self.printConnectedPeers)
            l.start(2)

    def printConnectedPeers(self):
        print(self.peers.peers)


class Sock(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        WebSocketServerProtocol.__init__(self, *args, **kwargs)

    def onConnect(self, request):
        print("Client connected: " + str(request))
        print(pprint(self.__dict__))

    def onOpen(self):
        print("Socket connection open")
        self.peerManager = self.transport.factory.wrappedFactory.peers

        self.sid = uuid.uuid4().hex

        self.peerManager.add(
            self.sid,
            self
        )

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: %d bytes." % len(payload))

        else:
            print("text message received: " + payload)

        try:
            payload = json.loads(payload)

        except:
            payload = None

        if payload is not None:

            method = payload['method']

            if method == 'offer':
                self.peerManager.push({
                    'type': 'offer',
                    'offer': payload['offer'],
                    'from': self.sid
                }, payload['to'])

            elif method == 'answer':
                self.peerManager.push({
                    'type': 'answer',
                    'answer': payload['answer'],
                    'from': self.sid
                }, payload['to'])

            elif method == 'ice':
                self.peerManager.push({
                    'type': 'ice',
                    'ice': payload['ice'],
                    'from': self.sid
                }, payload['to'])

            elif method == 'getPeers':
                ret = {
                    'type': 'peers',
                    'peers': self.peerManager.getPeers(who=self.sid)
                }
                self.sendMessage(json.dumps(ret))

            else:
                pass

    def onClose(self, wasClean, code, reason):
        print("Websocket connection closed")
        print(wasClean, code, reason)
        self.peerManager.remove(self.sid)

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    contextFactory = ssl.DefaultOpenSSLContextFactory(
        '/etc/ssl/private/mediacenter.key',
        '/etc/ssl/certs/ytdjb.com'
    )

    factory = SocketServerFactory('wss://127.0.0.1:8080')

    factory.protocol = Sock

    reactor.listenSSL(8080, factory, contextFactory)

    os.setuid(33)

    reactor.run()
