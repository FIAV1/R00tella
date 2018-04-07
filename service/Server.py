#!/usr/bin/env python

import socket
import sys
from threading import Thread
from handler.HandlerInterface import HandlerInterface
from threading import Timer
from utils import shell_colors


class Server:

	def __init__(self, port: int, handler: HandlerInterface):
		self.ss = None
		self.port = port
		self.BUFF_SIZE = 200
		self.handler = handler

	def child(self, sd) -> None:
		""" Serves the incoming requests/responses
		:param sd: socket descriptor
		:return: None
		"""
		self.handler.serve(sd)

	def __create_socket(self) -> None:
		""" Create the passive socket

		:return: None
		"""
		try:
			# Create the socket
			self.ss = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		except OSError as e:
			shell_colors.print_red(f'\nCan\'t create the socket: {e}\n')
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
			shell_colors.print_red(f'\nCan\'t handle the socket: {OSError}\n')
			sys.exit(socket.error)

	def __close_socket(self) -> None:
		""" Close the passive socket ending the accept

		:return: None
		"""
		try:
			self.ss.shutdown(2)
			self.ss.close()
		except OSError:
			self.ss.close()

	def run(self, temporary: bool) -> None:
		""" Execute the server that listens for incoming requests/repsonses

		:param temporary: indicate wether the server is temporary or not
		:return: None
		"""
		threads = []
		self.__create_socket()

		if temporary:
			timer = Timer(20, self.__close_socket)
			timer.start()

		while True:
			# Put the passive socket on hold for connection requests
			try:
				(sd, clientaddr) = self.ss.accept()

				if not temporary or (temporary and timer.is_alive()):
					t = Thread(target=self.child, args=sd)
					t.daemon = True
					t.start()
					threads.append(t)
				else:
					break

			except OSError:
				if threads is not None:
					for t in threads:
						t.join()
				break
