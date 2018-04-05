#!/usr/bin/env python

import socket
import os
import random


class Downloader:

	def __init__(self, host_ip4: str, host_ip6: str, host_port: int, request: str, file_name: str):
		self.host_ip4 = host_ip4
		self.host_ip6 = host_ip6
		self.host_port = host_port
		self.request = request
		self.file_name = file_name

	def __create_socket(self) -> (socket.socket, int):
		""" Create the active socket
		:return: the active socket and the version
		"""
		# Create the socket
		if random.random() <= 0.5:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			version = 4
		else:
			sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			version = 6

		return sock, version

	def __send_request(self, ip4_peer: str, ip6_peer: str, port_peer: int, request: str) -> socket.socket:
		""" Send the request to the specified host
		:param ip4_peer: host's ipv4 address
		:param ip6_peer: host's ipv6 address
		:param port_peer: host's port
		:param request: packet to be sent
		:return: sock: the socket which will receive the response
		"""
		sock, version = self.__create_socket()

		if version == 4:
			sock.connect((ip4_peer, port_peer))
		else:
			sock.connect((ip6_peer, port_peer))

		sock.send(request.encode())

		return sock

	def start(self):

		"""request = 'RETR' + self.file_md5
		self.sd.send(request.encode())

		ack = self.sd.recv(4).decode()
		if ack != "ARET":
			print('Whoops, something went wrong!')
			self.sd.close()"""

		try:
			sock = self.__send_request(self.host_ip4, self.host_ip6, self.host_port, self.request)
		except socket.error as e:
			print(f'Impossible to send data to {self.host_ip4}|{self.host_ip6} on port {self.host_port}:\n {e}')
			return

		total_chunks = int(sock.recv(6).decode())
		print(f'#chunk: {total_chunks}')
		try:
			fd = os.open('shared/' + self.file_name, os.O_WRONLY | os.O_CREAT)
		except OSError as e:
			print(f'Something went wrong: {e}')
			raise e

		for i in range(total_chunks):
			chunk_size = int(sock.recv(5).decode())
			data = sock.recv(chunk_size)
			os.write(fd, data)
		os.close(fd)
