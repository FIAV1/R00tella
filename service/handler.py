#!/usr/bin/env python

import socket
import os
from service.Uploader import Uploader

db_file = 'directory.db'


def serve(sd: socket.socket, request: bytes) -> str:
	""" Handle the peer request
	Parameters:
		request - the list containing the request parameters
	Returns:
		str - the response
	"""
	command = request[0:4].decode('UTF-8')

	if command == "QUER":

		return "This is the response for QUER"

	elif command == "NEAR":

		return "This is the response for NEAR"

	elif command == "RETR":

		if len(request) != 36:
			return "Invalid request, usage is..."

		file_md5 = request[5:36].decode()

		test_fd = os.open('shared/screen.png', os.O_RDONLY)

		Uploader(sd, test_fd).start()

		return "This is the response for RETR"

	else:
		return "Command \'" + request.decode('UTF-8') + "\' is invalid, try again."
