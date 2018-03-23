#!/usr/bin/env python

from multiprocessing import Process
from service.Server import Server
from .SelfHandler import SelfHandler
from threading import Timer


class Peer:

	def __init__(self, port: int):
		self.port = port

	def __create_socket(self):
		pass

	def __kill_server(self, p: Process):
		p.terminate()

	def __query(self):

		#codice che manda il pkt sulla socket

		#avvio il server di ricezione delle response
		p = Process(target=lambda: Server(self.port, SelfHandler()).run())
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

	def run(self):
		self.__create_socket()

