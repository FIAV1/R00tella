#!/usr/bin/env python
import socket
from handler.HandlerInterface import HandlerInterface


class SelfHandler(HandlerInterface):

	def serve(self, request: str, sd: socket.socket) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		command = request[:4]

		if command == "AQUE":
			pass

		elif command == "ANEA":
			pass

		elif command == "ARET":
			pass

		sd.close()
