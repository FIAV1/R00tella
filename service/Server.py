#!/usr/bin/env python

import socket
import sys
import os
from threading import Thread
from handler.HandlerInterface import HandlerInterface
from utils import hasher


class Server:

	def __init__(self, port: int, handler: HandlerInterface):
		self.ss = None
		self.port = port
		self.BUFF_SIZE = 200
		self.handler = handler

	def child(self, sd, clientaddr):
		# self.ss.close()

		request = sd.recv(self.BUFF_SIZE).decode()
		response = self.handler.serve(request, sd)

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

	# def __create_files_dictionary(self):
	#	for dir_entry in os.scandir('shared'):
	#		self.files_dict[dir_entry.name] = {'md5': hasher.get_md5(dir_entry.path), 'size': dir_entry.stat().st_size}

	def run(self):
		self.__create_socket()
		#print(f'Server {self.ss.getsockname()[0]} listening on port {self.ss.getsockname()[1]}...')

		while True:
			# Put the passive socket on hold for connection requests
			(sd, clientaddr) = self.ss.accept()

			t = Thread(target=self.child, args=(sd, clientaddr))
			t.daemon = True
			t.start()

			# essendo thread non c'è più bisogno di chiudere i fd: sono unici e condivisi
			# sd.close()
