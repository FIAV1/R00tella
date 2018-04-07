#!/usr/bin/env python

from handler.SelfHandler import SelfHandler
from service.Server import Server
from threading import Thread
import socket
import uuid
from service.AppData import AppData
import random
from service.Downloader import Downloader
from utils import net_utils
from utils import shell_colors


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

	def __unicast(self, ip4_peer: str, ip6_peer: str, port_peer: int, packet: str) -> None:
		""" Send the packet to the specified host

		:param ip4_peer: host's ipv4 address
		:param ip6_peer: host's ipv6 address
		:param port_peer: host's port
		:param packet: packet to be sent
		:return: None
		"""
		try:
			(sock, version) = self.__create_socket()

			if version == 4:
				sock.connect((ip4_peer, port_peer))
			else:
				sock.connect((ip6_peer, port_peer))

			sock.send(packet.encode())
			sock.close()
		except socket.error as e:
			shell_colors.print_red(f'\nImpossible to send data to {ip4_peer}|{ip6_peer} [{port_peer}]: {e}\n')
			return

	def __broadcast(self, packet: str) -> None:
		""" Send the packet to a pool of hosts

		:param packet: packet to be sent
		:return: None
		"""
		neighbours = AppData.get_neighbours()

		for neighbour in neighbours:
			self.__unicast(
				AppData.get_peer_ip4(neighbour),
				AppData.get_peer_ip6(neighbour),
				AppData.get_peer_port(neighbour),
				packet)

	def serve(self, choice: str) -> None:
		""" Handle the peer packet

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

				if not 0 <= len(search) <= 20:
					shell_colors.print_red('\nFile name must be between 1 and 20 chars long.\n')
					continue
				break

			packet = choice + pktid + ip + str(port).zfill(5) + ttl + search.ljust(20)
			AppData.add_query(choice, pktid, '')

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(port, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(packet)

			# grazie alla join possiamo aspettare la fine dell'esecuzione di un thread (il server che riceve tutte le risposte)
			t.join()

			files = AppData.get_peer_files()

			if len(files) < 1:
				shell_colors.print_yellow('\nFile not found.\n')
				return

			shell_colors.print_green(f'\n{len(files)} files found:')
			for count, file in enumerate(files, start=1):
				print(f'{count}]', file)

			while True:
				index = input('\nPlease select a file to download:')
				try:
					index = int(index)
					if 1 <= index <= len(files):
						break
					else:
						shell_colors.print_red(f'Index chosen must be in the correct range: 1 - {len(files)}.\n')
				except ValueError:
					shell_colors.print_red(f'Your choice must be a valid one: number in range 1 - {len(files)} expected.\n')

			host_ip4 = AppData.get_file_owner_ip4(files[index-1])
			host_ip6 = AppData.get_file_owner_ip6(files[index-1])
			host_port = AppData.get_file_owner_port(files[index-1])
			file_md5 = AppData.get_file_md5(files[index-1])
			file_name = AppData.get_file_name(files[index-1])

			# preparo packet per retr, faccio partire server in attesa download, invio packet e attendo
			packet = 'RETR' + file_md5

			try:
				Downloader(host_ip4, host_ip6, host_port, packet, file_name).start()

				shell_colors.print_green(f'\nDownload of {file_name} completed.\n')
				AppData.clear_peer_files()
			except Exception:
				shell_colors.print_red(f'\nError while downloading {file_name}\n')

		elif choice == "NEAR":
			# NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = net_utils.get_local_ip_for_response()
			port = net_utils.get_anea_port()
			ttl = '03'

			packet = choice + pktid + ip + str(port).zfill(5) + ttl
			AppData.add_query(choice, pktid, '')

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			t = Thread(target=lambda: Server(port, SelfHandler()).run(True))
			t.daemon = True
			t.start()

			self.__broadcast(packet)
			t.join()

		else:
			pass
