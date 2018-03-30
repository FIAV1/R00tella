#!/usr/bin/env python

import socket
import os


class Downloader:

	def __init__(self, sd: socket.socket, file_name: str):
		self.file_name = file_name
		self.sd = sd

	def start(self):

		"""request = 'RETR' + self.file_md5
		self.sd.send(request.encode())

		ack = self.sd.recv(4).decode()
		if ack != "ARET":
			print('Whoops, something went wrong!')
			self.sd.close()"""

		total_chunks = int(self.sd.recv(6).decode())
		print(f'#chunk: {total_chunks}')
		try:
			fd = os.open('shared/' + self.file_name, os.O_WRONLY | os.O_CREAT)
		except OSError as e:
			print(f'Something went wrong: {e}')
			raise e

		for i in range(total_chunks):
			chunk_size = int(self.sd.recv(5).decode())
			data = self.sd.recv(chunk_size)
			os.write(fd, data)
		os.close(fd)
