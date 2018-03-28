#!/usr/bin/env python

import socket
from service.AppData import AppData
import os
import stat


class Uploader:

	def __init__(self, sd: socket.socket, file_md5):
		self.sd = sd
		self.file_md5 = file_md5

	def start(self):
		file_name = AppData.get_filename_by_filemd5_on_shared_files(self.file_md5)
		if file_name is None:
			print('The requested file is not available')
		try:
			fd = os.open('shared/' + file_name, os.O_RDONLY)
			filesize = os.fstat(fd)[stat.ST_SIZE]
		except OSError as e:
			print(f'Something went wrong: {e}')
			raise

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
			data = os.read(fd, 4096)
			readed_size = str(len(data)).zfill(5)
			print(f'invio {readed_size} {data}')
			self.sd.send(readed_size.encode() + data)
