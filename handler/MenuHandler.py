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
from utils import net_utils


class MenuHandler:

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

	def __unicast(self, ip4_peer: str, ip6_peer: str, port_peer: int, request: str) -> None:
		""" Send the request to the specified host
		:param ip4_peer: host's ipv4 address
		:param ip6_peer: host's ipv6 address
		:param port_peer: host's port
		:param request: packet to be sent
		:return: None
		"""
		try:
			(sock, version) = self.__create_socket()

			if version == 4:
				sock.connect((ip4_peer, port_peer))
			else:
				sock.connect((ip6_peer, port_peer))

			sock.send(request.encode())
			sock.close()
		except socket.error as e:
			print(f'Impossible to send data to {ip4_peer}|{ip6_peer} on port {port_peer}: {e}')
			return

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
			ip = net_utils.get_local_ip_for_response()
			port = net_utils.get_aque_port()
			ttl = '50'

			while True:
				search = input('\nEnter the file name: ')

				if len(search) <= 0 or len(search) > 20:
					print('File name must be between 1 and 20 chars long.\n')
					return
				elif len(search) < 20:
					search.ljust(20)
					break
				else:
					break

			request = choice + pktid + ip + str(port).zfill(5) + ttl + search

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(port, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(request)

			# grazie alla join possiamo aspettare la fine dell'esecuzione di un thread (il server che riceve tutte le risposte)
			t.join()

			files = AppData.get_peer_files()

			if len(files) < 1:
				print('File not found.\n')
				return

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
					print('Your choice must be a valid one: number in range 1 - {len(files} expected\n')

			host_ip4 = AppData.get_peer_ip4(files[index])
			host_ip6 = AppData.get_peer_ip6(files[index])
			host_port = AppData.get_peer_port(files[index])
			file_md5 = AppData.get_file_md5(files[index])
			file_name = AppData.get_file_name(files[index])

			# preparo request per retr, faccio partire server in attesa download, invio request e attendo
			request = 'RETR' + file_md5 + file_name

			Downloader(host_ip4, host_ip6, host_port, request, file_name).start()

			print(f'Download of {file_name} completed.')
			AppData.clear_peer_files()

		elif choice == "NEAR":
			# NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = net_utils.get_local_ip_for_response()
			port = net_utils.get_anea_port()
			ttl = '03'

			request = choice + pktid + ip + str(port).zfill(5) + ttl

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(port, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(request)
			t.join()

		else:
			pass
