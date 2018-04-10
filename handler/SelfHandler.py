#!/usr/bin/env python

import socket
from utils import net_utils
from utils import shell_colors
from service.AppData import AppData
from handler.HandlerInterface import HandlerInterface


class SelfHandler(HandlerInterface):

	def serve(self, sd: socket.socket) -> None:
		""" Handle the peer request

		:param sd: the socket descriptor used for read the request
		:return None
		"""
		try:
			command = sd.recv(4).decode()
		except OSError as e:
			shell_colors.print_red(f'\nUnable to read the command from the socket: {e}\n')
			sd.close()
			return

		if command == "AQUE":
			try:
				response = sd.recv(300).decode()
			except socket.error as e:
				shell_colors.print_red(f'\nUnable to read the {command} response from the socket: {e}\n')
				sd.close()
				return

			sd.close()

			if len(response) != 208:
				print(f"\nInvalid response: {command} -> {response}. Expected: AQUE<pkt_id><ip_peer><port_peer><fileMD5><filename>\n")
				return

			pktid = response[0:16]
			ip_peer = response[16:71]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = int(response[71:76])
			filemd5 = response[76:108]
			filename = response[108:208].lower().lstrip().rstrip()

			if pktid != AppData.get_sent_packet():
				sd.close()
				return

			if not AppData.exist_peer_files(ip4_peer, ip6_peer, port_peer, filemd5, filename):
				AppData.add_peer_files(ip4_peer, ip6_peer, port_peer, filemd5, filename)
				index = AppData.peer_file_index(ip4_peer, ip6_peer, port_peer, filemd5, filename)
				print(f'{index}] ', end='')
				shell_colors.print_blue(f'{filename} ', end='')
				shell_colors.print_yellow(f'md5={filemd5} ', end='')
				print(f'({ip4_peer}|{ip6_peer} [{port_peer}])')

		elif command == "ANEA":
			try:
				response = sd.recv(300).decode()
			except socket.error as e:
				shell_colors.print_red(f'\nUnable to read the {command} response from the socket: {e}\n')
				sd.close()
				return

			sd.close()

			if len(response) != 76:
				shell_colors.print_red(f"\nInvalid response: : {command} -> {response}. Expected: ANEA<pkt_id><ip_peer><port_peer>")
				return

			pktid = response[0:16]
			ip_peer = response[16:71]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = int(response[71:76])

			if pktid != AppData.get_sent_packet():
				return

			if len(AppData.get_neighbours()) >= 5:
				return

			if not AppData.is_neighbour(ip4_peer, ip6_peer, port_peer):
				AppData.add_neighbour(ip4_peer, ip6_peer, port_peer)
				index = AppData.neighbour_index(ip4_peer, ip6_peer, port_peer)
				print(f'{index}] New neighbour found: {ip4_peer}|{ip6_peer} [{port_peer}]')

		else:
			wrong_response = sd.recv(300).decode()
			sd.close()
			shell_colors.print_red(f"\nInvalid response: {command} -> {wrong_response}\n")

		return
