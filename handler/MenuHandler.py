#!/usr/bin/env python
from handler.SelfHandler import SelfHandler
from handler.HandlerInterface import HandlerInterface
from service.Server import Server
from threading import Timer
import socket
from multiprocessing import Process


class MenuHandler(HandlerInterface):

	def __kill_server(self, p: Process):
		p.terminate()

	def serve(self, request: str, sd: socket.socket) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		command = request[:4]

		if command == "QUER":
			# codice che manda il pkt sulla socket

			# avvio il server di ricezione delle response
			p = Process(target=lambda: Server(4000, SelfHandler()).run())
			p.daemon = True
			p.start()

			# avvio il timer
			t = Timer(300, self.__kill_server, args=(p,))
			t.start()

			input('\nRicerca file in corso, premere invio per continuare...\n')

			if t.isAlive:
				t.cancel()
				self.__kill_server(p)

			choice = input('Scegli da chi scaricare:')

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
