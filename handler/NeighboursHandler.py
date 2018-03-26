#!/usr/bin/env python

import socket
import random
from handler.HandlerInterface import HandlerInterface
from service.AppData import AppData
from utils import ip_utils
from threading import Timer


class NeighboursHandler(HandlerInterface):

	def __delete_packet(self, pktid: str):
		if AppData.exist_packet(pktid):
			del AppData.packets[pktid]

	def __create_socket(self):
		if random.random() <= 0.5:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			version = 4
		else:
			sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			version = 6

		return sock, version

	def serve(self, request: str, sd: socket.socket):
		""" Handle the neighbours requests

		:param request: the string containing the request
		:param sd: the socket descriptor used for upload a file in case of RETR request
		:return: None
		"""
		command = request[:4]

		if command == "QUER":
			if len(request) != 102:
				return "Invalid request. Usage is: QUER<pkt_id><your_ip><your_port><ttl><query>"

			pktid = request[4:20]
			ip_peer = request[20:75]
			ip4_peer, ip6_peer = ip_utils.get_ip_pair(ip_peer)
			port_peer = request[75:80]
			ttl = request[80:82]
			query = request[82:102]

			# packet management
			if not AppData.exist_packet(pktid):
				AppData.add_packet(pktid, ip_peer, port_peer)
				t = Timer(300, function=self.__delete_packet, args=(pktid,))
				t.start()

			# search for the requested file
			results = AppData.search_in_shared_files(query)

			for file in results:
				response = 'AQUE' +\
						pktid + ip_peer + port_peer +\
						AppData.get_shared_filemd5(file) +\
						AppData.get_shared_filename(file).ljust(100)

				sock, version = self.__create_socket()
				if version == 4:
					sock.connect((ip4_peer, port_peer))
				else:
					sock.connect((ip6_peer, port_peer))
				sock.send(response.encode())
				sock.close()

			# forwarding the packet to other peers
			new_ttl = int(ttl) - 1

			if new_ttl > 0:
				peer = (ip4_peer, ip6_peer, port_peer)
				recipients = AppData.neighbours
				if AppData.is_neighbour(peer):
					recipients.remove(peer)

				request.replace(ttl, str(new_ttl).zfill(3))

				for peer in recipients:
					sock, version = self.__create_socket()
					if version == 4:
						sock.connect((AppData.get_peer_ip4(peer), AppData.get_peer_port(peer)))
					else:
						sock.connect((AppData.get_peer_ip6(peer), AppData.get_peer_port(peer)))
					sock.send(request.encode())
					sock.close()

		elif command == "NEAR":
			pass

		elif command == "RETR":

			if len(request) != 36:
				return "Invalid request, usage is RETR<Filemd5>"

			file_md5 = request[5:36].decode()

			test_fd = os.open('shared/screen.png', os.O_RDONLY)

			#Uploader(sd, test_fd).start()

		else:
			pass

		sd.close()
