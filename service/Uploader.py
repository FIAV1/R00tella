#!/usr/bin/env python

import socket
import os
import stat


class Uploader:

	def __init__(self, sd: socket.socket, fd: int):
		self.sd = sd
		self.fd = fd

	def start(self):

		filesize = os.fstat(self.fd)[stat.ST_SIZE]

		# Calcolo i chunk
		nchunk = filesize / 4096
		# Verifico se il file si divide esattamente nei chunk
		if (filesize % 4096) != 0:
			nchunk = nchunk + 1

		nchunk = int(nchunk)

		# Invio identificativo al peer
		response = "ARET" + str(nchunk).zfill(6)
		self.sd.send(response.encode())

		for i in range(nchunk):
			size = '04096'
			data = os.read(self.fd, 4096)
			print(f'invio {size} {data}')
			self.sd.send(size.encode() + data)
