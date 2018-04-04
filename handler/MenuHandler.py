#!/usr/bin/env python

from handler.SelfHandler import SelfHandler
from service.Server import Server
from threading import Thread
import socket
import uuid
from service.AppData import AppData
from typing import Optional
import random
from service.Downloader import Downloader


class MenuHandler:

	def __create_socket(self) -> Optional[socket.socket, int]:
		""" Create the active socket

		:return: the active socket
		"""
		try:
			# Create the socket
			if random.random() <= 0.5:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				version = 4
			else:
				sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
				version = 6

			return sock, version
		except OSError as e:
			print(f'\nCan\'t create the socket: {e}\n')
			return None

	def __unicast(self, ip4_peer: str, ip6_peer: str, port_peer: str, request: str) -> Optional[socket.socket, int]:
		""" Send the request to the specified host

		:param ip4_peer: host's ipv4 address
		:param ip6_peer: host's ipv6 address
		:param port_peer: host's port
		:param request: packet to be sent
		:return: the socket and the ip version
		"""
		try:
			(sock, version) = self.__create_socket()

			if (sock, version) not in None:
				if version == 4:
					sock.connect((ip4_peer, port_peer))
					ip = ip4_peer
				else:
					sock.connect((ip6_peer, port_peer))
					ip = ip6_peer
				port = port_peer

				sock.send(request.encode())
				sock.close()

				return sock, version
			else:
				return None, None
		except socket.error as e:
			print(f'Impossible to send data to {ip} on port {port}:\n {e}')
			return None, None

	def __broadcast(self, request: str) -> None:
		""" Send the request to a pool of hosts

		:param request: the request to send
		:return: None
		"""
		neighbours = AppData.get_neighbours()

		for neighbour in neighbours:
			self.__unicast(
				AppData.get_peer_ip4(neighbour),
				AppData.get_peer_ip6(neighbour),
				AppData.get_peer_port(neighbour),
				request)

	def serve(self, choice: str) -> None:
		""" Handle the peer request

		:param choice: the choice to handle
		:return: None
		"""

		if choice == "QUER":

			# codice che manda il pkt sulla socket
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = '172.016.001.001|FC00:2001:db8a:a0b2:12f0:a13w:0001:0001'
			port = '4000'

			search = input('\nEnter the file name: ')

			# aggiungere verifica lunghezza file name
			if len(search) <= 0 or len(search) > 20:
				print('File name must be between 1 and 20 chars long.\n')
				return
			elif len(search) < 20:
				# codice per riempire la search con spazi se necessario
				zfill = 20 - len(search)
				search = search + (' ' * zfill)

			request = choice+pktid+ip+port+search

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(int(port), SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(request)

			# grazie alla join possiamo aspettare la fine dell'esecuzione di un thread (il server che riceve tutte le risposte)
			t.join()

			files = AppData.get_peer_files()

			for count, file in enumerate(files, start=1):
				print(f'{count}]', file)

			while True:
				index = input('Please select a file to download:')
				try:
					index = int(index)
					if 1 <= index < len(files):
						break
					else:
						print(f'Index chosen must be in the correct range: 1 - {len(files)}\n')
				except ValueError:
					print('Your choice must be a valid one. Number in range 1 - {len(files} expected\n')

			host = (AppData.get_peer_ip4(files[index]), AppData.get_peer_ip6(files[index]), AppData.get_peer_port(files[index]))
			file_md5 = AppData.get_file_md5(files[index])
			file_name = AppData.get_file_name(files[index])

			# preparo request per retr, faccio partire server in attesa download, invio request e attendo
			request = 'RETR'+file_md5+file_name

			(sock, port) = self.__unicast(host, request)
			Downloader.start(sock, port, AppData.get_file_download())

			print(f'Download of {file_name} completed.')

		elif choice == "NEAR":
			# NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = '172.016.001.001|FC00:2001:db8a:a0b2:12f0:a13w:0001:0001'
			port = '4001'
			ttl = '3'

			request = choice + pktid + ip + port + ttl

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(int(port), SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(request)
			t.join()

			neighbours = AppData.get_neighbours()
			print(f'Sono stati aggiunti {len(neighbours)} vicini:\n')
			for count, neighbour in enumerate(neighbours, start=1):
				print(f'{neighbour}\n')

		else:
			pass
