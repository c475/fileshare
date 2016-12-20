import sys

sys.path.append('/srv/')
sys.path.append('/srv/server/')
sys.path.append('/srv/fileshare/')
sys.path.append('/srv/client/')

from django.conf import settings
from django import setup

settings.configure()
setup()

from twisted.python import log
from twisted.internet import ssl

from autobahn.twisted.websocket import (
	WebSocketServerProtocol,
	WebSocketServerFactory,
	listenWS
)


class Socks(WebSocketServerProtocol):

	def onConnect(self, request):
		print("Client connected: " + str(request.__dict__))

	def onOpen(self):
		print("Socket connection open")

	def onMessage(self, payload, isBinary):
		if isBinary:
			print("Binary message received: %d bytes." % len(payload))

		else:
			print("text message received: " + payload)

		self.sendMessage(payload, isBinary)

	def onClose(self, wasClean, code, reason):
		print("Websocket connection closed")
		print(wasClean, code, reason)


if __name__ == '__main__':

	log.startLogging(sys.stdout)

	contextFactory = ssl.DefaultOpenSSLContextFactory(
		'/etc/ssl/private/mediacenter.key',
		'/etc/ssl/certs/ytdjb.com'
	)

	factory = WebSocketServerFactory('ws://127.0.0.1:8080')
	
	factory.setProtocolOptions(
		allowedOrigins=[
			'https://127.0.0.1',
			'https://ytdjb.com'
		]
	)

	factory.protocol = Socks

	listenWS(factory, contextFactory)
