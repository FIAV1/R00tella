#!/usr/bin/env python

import socket
import sys


class Downloader:

	def __init__(self, ip: str, port: int, file_md5: str):
		self.ip = ip
		self.port = port
		self.file_md5 = file_md5
		self.sd = None

	def __handle(self):

		request = 'RETR' + self.file_md5
		self.sd.send(request.encode())

		ack = self.sd.recv(4).decode()
		if ack != "ARET":
			print('Whoops, something went wrong!')
			self.sd.close()

		total_chunks = int(self.sd.recv(6).decode())
		f = open('pippo', 'wb')

		for i in range(total_chunks):
			chunk_size = int(self.sd.recv(5).decode())
			data = self.sd.recv(chunk_size)
			f.write(data)

	def start(self):
		try:
			# Create the socket
			self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except OSError as e:
			print(f'Can\'t create the socket: {e}')
			sys.exit(socket.error)

		try:
			# connect to the peer
			self.sd.connect((self.ip, self.port))
			print(f'Download starting from {self.ip}[{self.port}]...')
		except OSError as e:
			print(f'Connection error: {e}')
			sys.exit(socket.error)

		self.__handle()
