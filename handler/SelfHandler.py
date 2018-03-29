#!/usr/bin/env python

import socket
from utils import ip_utils
from service.AppData import AppData
from handler.HandlerInterface import HandlerInterface
from service.Downloader import Downloader


class SelfHandler(HandlerInterface):

	def serve(self, response: str, sd: socket.socket) -> None:
		""" Handle the peer request
		Parameters:
			request - the list containing the request parameters
		Returns:
			str - the response
		"""
		try:
			command = sd.recv(4).decode()
		except OSError as e:
			print(f'Unable to read the command from the socket\n OSError: {e}')

		if command == "AQUE":

			try:
				response = sd.recv(208).decode()
			except OSError as e:
					print(f'Unable to read the {command} response from the socket\n OSError: {e}')


			if len(response) != 208:
				return "Invalid response. Expected: AQUE<pkt_id><ip_peer><port_peer><fileMD5><filename>"

			pktid = response[0:16]
			ip_peer = response[16:71]
			ip4_peer, ip6_peer = ip_utils.get_ip_pair(ip_peer)
			port_peer = response[71:76]
			filemd5 = response[76:108]
			filename = response[108:208].lower().lstrip().rstrip()

			if not AppData.exist_packet(pktid):
				AppData.add_packet(pktid, ip_peer, port_peer)

			if not AppData.exist_peer_files((ip4_peer, ip6_peer, port_peer, filemd5, filename)):
				AppData.add_peer_files((ip4_peer, ip6_peer, port_peer, filemd5, filename))

			index = AppData.peer_file_index((ip4_peer, ip6_peer, port_peer, filemd5, filename))

			print(f'{index})   Response from {ip4_peer}|{ip6_peer} port {port_peer} --> File: {filename} MD5: {filemd5}')


		elif command == "ANEA":

			try:
				response = sd.recv(76).decode()
			except OSError as e:
					print(f'Unable to read the {command} response from the socket\n OSError: {e}')

			if len(response) != 76:
				return "Invalid response. Expected: ANEA<pkt_id><ip_peer><port_peer>"

			pktid = response[0:16]
			ip_peer = response[16:71]
			ip4_peer, ip6_peer = ip_utils.get_ip_pair(ip_peer)
			port_peer = response[71:76]

			if not AppData.exist_packet(pktid):
				AppData.add_packet(pktid, ip_peer, port_peer)

			if not AppData.is_neighbour((ip4_peer,ip6_peer,port_peer)):
				AppData.add_neighbour((ip4_peer,ip6_peer,port_peer))

			print(f'New neighbour founded: {ip4_peer}|{ip6_peer} port {port_peer}')

		elif command == "ARET":

			#if len(request) <= 15:
			#	return "Invalid response. Expected: ARET<#chunks>{<chunk_lenght(i)><data(i)>} for i=1,2,...,#chunks"

			Downloader.start(sd, AppData.get_file_download())

		sd.close()
