#!/usr/bin/env python

import socket
import sys
import os
import multiprocessing
from . import handler
from utils import shell_colors as shell


class Server:

	def __init__(self, port: int):
		self.port = port
		self.ss = None
		self.BUFF_SIZE = 200

	def child(self, sd, clientaddr):
		(client, client_port) = socket.getnameinfo(clientaddr, socket.NI_NUMERICHOST)
		self.ss.close()

		request = sd.recv(self.BUFF_SIZE)
		shell.print_green(f'{client} [{client_port}] -> ', end='')
		print(f'{request.decode()}', end='')

		response = handler.serve(sd, request)
		shell.print_red(' -> ', end='')
		print(f'{response}')

		sd.close()
		os._exit(0)

	def __create_socket(self):
		try:
			# Create the socket
			self.ss = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		except OSError as e:
			print(f'Can\'t create the socket: {e}')
			sys.exit(socket.error)

		try:
			# Set the SO_REUSEADDR flag in order to tell the kernel to reuse the socket even if it's in a TIME_WAIT state,
			# without waiting for its natural timeout to expire.
			# This is because sockets in a TIME_WAIT state can’t be immediately reused.
			self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.ss.setsockopt(41, socket.IPV6_V6ONLY, 0)

			# Bind the local address (sockaddr) to the socket (ss)
			self.ss.bind(('', self.port))

			# Transform the socket in a passive socket and
			# define a queue of SOMAXCONN possible connection requests
			self.ss.listen(socket.SOMAXCONN)
		except OSError:
			print(f'Can\'t handle the socket: {OSError}')
			sys.exit(socket.error)

	def run(self):
		self.__create_socket()
		print(f'Server {self.ss.getsockname()[0]} listening on port {self.ss.getsockname()[1]}...')

		while True:
			# Put the passive socket on hold for connection requests
			(sd, clientaddr) = self.ss.accept()

			p = multiprocessing.Process(target=self.child, args=(sd, clientaddr,))
			p.daemon = True
			p.start()

			sd.close()
