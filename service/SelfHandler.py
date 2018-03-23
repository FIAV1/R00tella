#!/usr/bin/env python
import socket
from .HandlerInterface import HandlerInterface


class SelfHandler(HandlerInterface):

	def serve(self, sd: socket.socket) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		request = sd.recv(self.BUFF_SIZE)
		command = request[:4]

		if command == "AQUE":
			pass

		elif command == "ANEA":
			pass

		elif command == "ARET":
			pass

		sd.close()
