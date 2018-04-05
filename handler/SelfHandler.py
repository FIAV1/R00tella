#!/usr/bin/env python

import socket
from utils import net_utils
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
			print(f'Unable to read the command from the socket\n OSError: {e}')
			sd.close()
			return

		if command == "AQUE":
			try:
				response = sd.recv(300).decode()
			except socket.error as e:
				print(f'Unable to read the {command} response from the socket: {e}')
				sd.close()
				return

			sd.close()

			if len(response) != 208:
				print("Invalid response. Expected: AQUE<pkt_id><ip_peer><port_peer><fileMD5><filename>\nFrom the socket:" + command + response)
				return

			pktid = response[0:16]
			ip_peer = response[16:71]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = int(response[71:76])
			filemd5 = response[76:108]
			filename = response[108:208].lower().lstrip().rstrip()

			# TODO: controllare che il pktid sia coerente con il pktid della nostra QUER

			if not AppData.exist_peer_files(ip4_peer, ip6_peer, port_peer, filemd5, filename):
				AppData.add_peer_files(ip4_peer, ip6_peer, port_peer, filemd5, filename)

			index = AppData.peer_file_index(ip4_peer, ip6_peer, port_peer, filemd5, filename)

			print(f'{index}) Response from {ip4_peer}|{ip6_peer} port {port_peer} --> File: {filename} MD5: {filemd5}')

		elif command == "ANEA":
			try:
				response = sd.recv(300).decode()
			except socket.error as e:
				print(f'Unable to read the {command} response from the socket: {e}')
				sd.close()
				return

			sd.close()

			if len(response) != 76:
				print("Invalid response. Expected: ANEA<pkt_id><ip_peer><port_peer>\nFrom the socket:" + command + response)
				return

			pktid = response[0:16]
			ip_peer = response[16:71]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = int(response[71:76])

			# TODO: controllare che il pktid sia coerente con il pktid della nostra NEAR

			if not AppData.is_neighbour(ip4_peer, ip6_peer, port_peer):
				AppData.add_neighbour(ip4_peer, ip6_peer, port_peer)
				index = AppData.neighbour_index(ip4_peer, ip6_peer, port_peer)
				print(f'{index}) New neighbour found: {ip4_peer}|{ip6_peer} port {port_peer}')

		else:
			wrong_response = sd.recv(300).decode()
			sd.close()
			print("Invalid response.\nFrom the socket:" + command + wrong_response)

		return
