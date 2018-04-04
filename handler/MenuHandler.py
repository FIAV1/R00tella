#!/usr/bin/env python

from handler.SelfHandler import SelfHandler
from service.Server import Server
from threading import Thread
import socket
import uuid
from service.AppData import AppData
from typing import Optional
import random


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

	def __send_packet(self, ip4_peer: str, ip6_peer: str, port_peer: str, packet: str) -> (bool, str, str):
		""" Send the packet to the specified host

		:param ip4_peer: host's ipv4 address
		:param ip6_peer: host's ipv6 address
		:param port_peer: host's port
		:param packet: packet to be sent
		:return: bool indicating if the action succeeded or not, and host's ip and port
		"""
		try:
			sock, version = self.__create_socket()

			if (sock, version) not in None:
				if version == 4:
					sock.connect((ip4_peer, port_peer))
					# Parametri utili per debug e feedback nel caso di errori di comunicazione
					ip = ip4_peer
				else:
					sock.connect((ip6_peer, port_peer))
					ip = ip6_peer
				port = port_peer

				sock.send(packet.encode())
				sock.close()

				return True, ip, port
			else:
				return False, None, None
		except socket.error as e:
			print(f'Error while sending the packet: {e}')
			return False, None, None

	def __broadcast(self, request: str) -> None:
		""" Send the request to a pool of hosts

		:param request: the request to send
		:return: None
		"""
		neighbours = AppData.get_neighbours()

		for neighbour in neighbours:
			(success, ip, port) = self.__send_packet(
				AppData.get_peer_ip4(neighbour),
				AppData.get_peer_ip6(neighbour),
				AppData.get_peer_port(neighbour),
				request)
			if not success:
				print(f'Impossible to send data to {ip} on port {port}\n')

	def __unicast(self, host: tuple, request: str) -> None:
		""" Send the request to a single host

		:param host: host to send the request to
		:param request: the request to be sent
		:return: None
		"""
		(success, ip, port) = self.__send_packet(
			AppData.get_peer_ip4(host),
			AppData.get_peer_ip6(host),
			AppData.get_peer_port(host),
			request)
		if sd is not None:
			try:
				sd.sendall(request.encode())
				sd.close()
			except socket.error:
				print(f'Impossible to send data to {host} on port {port}\n')
		else:
			print(f'Cannot connect to {host} on port {port}\n')

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

			request = choice+pktid+ip+port+search

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(4000, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(request)

			# grazie alla join possiamo aspettare la fine dell'esecuzione di un thread (il server che riceve tutte le risposte)
			t.join()

			files = AppData.get_peer_files()

			for count, file in enumerate(files, start=1):
				print(f'{count}]', file)

			index = input('Please select a file to download:')
			host = (files[int(index)][0], files[int(index)][1], files[int(index)][2])
			file_md5 = files[int(index)][3]
			file_name = files[int(index)][4]

			# preparo request per retr, faccio partire server in attesa download, invio request e attendo
			request = 'RETR'+file_md5+file_name

			t = Thread(target=lambda: Server(4001, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__unicast(host, request)

			t.join()

			print(f'Download of {file_name} completed.')

		elif choice == "NEAR":
			# NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = '172.016.001.001|FC00:2001:db8a:a0b2:12f0:a13w:0001:0001'
			port = '4000'
			ttl = '3'

			request = choice + pktid + ip + port + ttl

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(4002, SelfHandler()).run(True))
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
