#!/usr/bin/env python

from handler.SelfHandler import SelfHandler
from service.ServerThread import ServerThread
import socket
import uuid
from service.AppData import AppData
import random
from service.Downloader import Downloader
from utils import net_utils
from utils import shell_colors
from threading import Timer
from utils.SpinnerThread import SpinnerThread
import os


class MenuHandler:

	def __create_socket(self) -> (socket.socket, int):
		""" Create the active socket

		:return: the active socket and the version
		"""
		# Create the socket
		if random.random() <= 0.5:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1)
			version = 4
		else:
			sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			sock.settimeout(1)
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
			pass
			# shell_colors.print_red(f'Impossible to send data to {ip4_peer}|{ip6_peer} [{port_peer}]: {e}\n')

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
			server = ServerThread(port, SelfHandler())
			server.daemon = True
			server.start()

			shell_colors.print_blue('\n! Press enter to continue !\n')
			spinner = SpinnerThread('Searching files', 'Results:')
			spinner.start()

			timer = Timer(300, lambda: (spinner.stop(), server.stop()))
			timer.start()

			self.__broadcast(packet)
			input()
			print('\033[1A', end='\r')

			if timer.is_alive():
				spinner.stop()
				spinner.join()
				timer.cancel()
				timer.join()
				server.stop()
				server.join()
			else:
				spinner.join()
				timer.join()
				server.join()

			files = AppData.get_peer_files()

			if len(files) < 1:
				shell_colors.print_red('\nNo matching results.\n')
				return

			for count, file in enumerate(files, start=1):
				print(f'{count}]', file)

			while True:
				index = input('\nPlease select a file to download: ')
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
				AppData.add_shared_file(file_name, file_md5, os.stat('shared/' + file_name).st_size)
			except OSError:
				shell_colors.print_red(f'\nError while downloading {file_name}\n')

		elif choice == "NEAR":
			# NEAR[4B].Packet_Id[16B].IP_Peer[55B].Port_Peer[5B].TTL[2B]
			pktid = str(uuid.uuid4().hex[:16].upper())
			ip = net_utils.get_local_ip_for_response()
			port = net_utils.get_anea_port()
			ttl = '03'

			packet = choice + pktid + ip + str(port).zfill(5) + ttl
			AppData.add_query(choice, pktid, '')

			old_neighbours_len = len(AppData.get_neighbours())

			# avvio il server di ricezione delle response, lo faccio prima del broadcast
			# per evitare che i primi client che rispondono non riescano a connettersi
			server = ServerThread(port, SelfHandler())
			server.daemon = True
			server.start()

			shell_colors.print_blue('\n! Press enter to continue !\n')
			spinner = SpinnerThread('Searching peers', 'Results:')
			spinner.start()

			timer = Timer(300, lambda: (spinner.stop(), server.stop()))
			timer.start()

			self.__broadcast(packet)
			input()
			print('\033[1A', end='\r')

			if timer.is_alive():
				spinner.stop()
				spinner.join()
				timer.cancel()
				timer.join()
				server.stop()
				server.join()
			else:
				spinner.join()
				timer.join()
				server.join()

			if len(AppData.get_neighbours()) == old_neighbours_len:
				shell_colors.print_red('\nNo new peer found.\n')

		elif choice == 'ADDPEER':
			net_utils.prompt_neighbours_request()

		elif choice == 'LISTPEERS':
			shell_colors.print_green('\nList of known peers:')
			for count, neighbour in enumerate(AppData.get_neighbours(), start=1):
				shell_colors.print_blue(f'{count}] {AppData.get_peer_ip4(neighbour)} {AppData.get_peer_ip6(neighbour)} {str(AppData.get_peer_port(neighbour))}')

		elif choice == 'REMOVEPEER':
			neighbours = AppData.get_neighbours()
			shell_colors.print_green('\nList of known peers:')
			for count, neighbour in enumerate(neighbours, start=1):
				shell_colors.print_blue(f'{count}] {AppData.get_peer_ip4(neighbour)} {AppData.get_peer_ip6(neighbour)} {str(AppData.get_peer_port(neighbour))}')

			while True:
				index = input('\nPlease select a peer to delete (q to cancel): ')
				if index == 'q':
					break

				try:
					index = int(index)
					if 1 <= index <= len(neighbours):
						AppData.remove_neighbour(index-1)
						break
					else:
						shell_colors.print_red(f'Index chosen must be in the correct range: 1 - {len(neighbours)}.\n')
				except ValueError:
					shell_colors.print_red(f'Your choice must be a valid one: number in range 1 - {len(neighbours)} expected.\n')

		else:
			pass
