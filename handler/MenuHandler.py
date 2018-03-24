#!/usr/bin/env python

from handler.SelfHandler import SelfHandler
from service.Server import Server
from threading import Timer
import socket
from multiprocessing import Process


class MenuHandler:

	def __kill_server(self, p: Process):
		p.terminate()

	def __create_socket(self):
		pass

	def __broadcast(self, request):
		# qua ci andrà il codice che in un ciclo invia la request ad ogni vicino
		# appoggiandosi a __create_socket per la creazione della socket necessaria
		# ad ogni iterazione
		pass

	def serve(self, choice: str) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""

		if choice == "QUER":
			# codice che manda il pkt sulla socket

			# avvio il server di ricezione delle response
			p = Process(target=lambda: Server(4000, SelfHandler()).run())
			p.daemon = True
			p.start()

			# avvio il timer
			t = Timer(300, self.__kill_server, args=(p,))
			t.start()

			input('\nFile search in progress, press enter to continue...\n')

			if t.isAlive:
				t.cancel()
				self.__kill_server(p)

			choice = input('Please select a peer:')

		elif choice == "NEAR":
			pass

		elif choice == "RETR":

			if len(request) != 36:
				return "Invalid request, usage is RETR<Filemd5>"

			file_md5 = request[5:36].decode()

			test_fd = os.open('shared/screen.png', os.O_RDONLY)

			#Uploader(sd, test_fd).start()

		else:
			pass