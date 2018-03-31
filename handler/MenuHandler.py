#!/usr/bin/env python

from handler.SelfHandler import SelfHandler
from service.Server import Server
from threading import Thread
import socket
import uuid
from service.AppData import AppData
from typing import Optional


class MenuHandler:

	@staticmethod
	def __create_socket(host: str, port: str) -> Optional[socket.socket]:
		""" Handle the peer request
		Parameters:
			host - ip address of the host
			port - port of the host
		Returns:
			socket - the active socket
		"""
		try:
			# Create the socket
			ss = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		except OSError as e:
			print(f'\nCan\'t create the socket: {e}\n')
			return None

		try:
			# Set the SO_REUSEADDR flag in order to tell the kernel to reuse the socket even if it's in a TIME_WAIT state,
			# without waiting for its natural timeout to expire.
			# This is because sockets in a TIME_WAIT state can’t be immediately reused.
			ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			ss.setsockopt(41, socket.IPV6_V6ONLY, 0)

			ss.connect((host, port))

			return ss
		except OSError as e:
			print(f'\nCan\'t handle the socket: {e}\n')
			return None

	@classmethod
	def __broadcast(cls, request: str):
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		"""
		neighbours = AppData.get_neighbours()

		for neighbour in neighbours:
			sd = cls.__create_socket(neighbour[0], neighbour[1])
			if sd is not None:
				try:
					sd.sendall(request.encode())
					sd.close()
				except socket.error:
					print(f'Impossible to send data to {neighbour[0]} on port {neighbour[1]}\n')
			else:
				print(f'Cannot connect to {neighbour[0]} on port {neighbour[1]}\n')

	@classmethod
	def __unicast(cls, host: str, port: str, request: str):
		sd = cls.__create_socket(host, port)
		if sd is not None:
			try:
				sd.sendall(request.encode())
				sd.close()
			except socket.error:
				print(f'Impossible to send data to {host} on port {port}\n')
		else:
			print(f'Cannot connect to {host} on port {port}\n')

	@classmethod
	def serve(cls, choice: str) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		print("Yeah! You chose: " + choice + "\n\n")

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

			cls.__broadcast(request)
			t.join()

			files = AppData.search_in_peer_files(search)

			for count, file in enumerate(files, start=1):
				print(f'{count}]', file)

			index = input('Please select a file to download:')
			if files[int(index)][0]:
				host = files[int(index)][0]
			else:
				host = files[int(index)][1]
			port = files[int(index)][2]
			file_md5 = files[int(index)][3]
			file_name = files[int(index)][4]

			# preparo request per retr, faccio partire server in attesa download, invio request e attendo
			request = 'RETR'+file_md5+file_name

			t = Thread(target=lambda: Server(4000, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			cls.__unicast(host, port, request)

			t.join()

			print(f'Download of {file_name} completed.')

		elif choice == "NEAR":
			# NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = '172.016.001.001|FC00:2001:db8a:a0b2:12f0:a13w:0001:0001'
			port = '4000'
			ttl = 3

			request = choice + pktid + ip + port + ttl

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(4000, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			cls.__broadcast(request)
			t.join()

			neighbours = AppData.get_neighbours()
			print(f'Sono stati aggiunti {len(neighbours)} vicini:\n')
			for count, neighbour in enumerate(neighbours, start=1):
				print(f'{neighbour}\n')

		else:
			pass
