#!/usr/bin/env python

import socket
from handler.HandlerInterface import HandlerInterface


class NeighboursHandler(HandlerInterface):

	def serve(self, request: str, sd: socket.socket) -> None:
		""" Handle the neighbours requests
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		command = request[:4]

		if command == "QUER":
			pass

		elif command == "NEAR":
			pass

		elif command == "RETR":

			if len(request) != 36:
				return "Invalid request, usage is RETR<Filemd5>"

			file_md5 = request[5:36].decode()

			test_fd = os.open('shared/screen.png', os.O_RDONLY)

			#Uploader(sd, test_fd).start()

		else:
			pass

		sd.close()
