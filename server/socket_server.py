from autobahn.twisted.websocket import (
	WebSocketServerProtocol,
	WebSocketServerFactory
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

	import sys

	from twisted.python import log
	from twisted.internet import reactor

	log.startLogging(sys.stdout)

	factory = WebSocketServerFactory('ws://127/0/0/1:9000')
	factory.protocol = Socks

	reactor.listenTCP(8080, factory)
	reactor.run()
