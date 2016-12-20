import os
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
from twisted.internet import (
	reactor,
	ssl
)

from autobahn.twisted.websocket import (
	WebSocketServerProtocol,
	WebSocketServerFactory
)


class Socks(WebSocketServerProtocol):

	def onConnect(self, request):
		print("Client connected: " + str(request))

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

	# Stupid bug in autobahn or twisted, this doesn't work
	# factory.setProtocolOptions(
	# 	allowedOrigins=[
	# 		'https://ytdjb.com'
	# 	]
	# )

	factory.protocol = Socks

	reactor.listenSSL(8080, factory, contextFactory)

	# switch back to www-data after opening certs
	os.setuid(33)

	reactor.run()
