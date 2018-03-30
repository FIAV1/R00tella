#!/usr/bin/env python

import socket
import random
from handler.HandlerInterface import HandlerInterface
from service.AppData import AppData
from service.Uploader import Uploader
from utils import net_utils, Logger
from threading import Timer
import os


class NeighboursHandler(HandlerInterface):

	def __init__(self, log: Logger.Logger):
		self.log = log

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

	def __forward_packet(self, ip_sender: str, ttl: str, packet: str):
		new_ttl = int(ttl) - 1

		if new_ttl > 0:
			# get the recipients list without the peer who sent the packet
			recipients = AppData.get_neighbours_recipients(ip_sender)

			packet.replace(ttl, str(new_ttl).zfill(3))

			for peer in recipients:
				self.__send_packet(AppData.get_peer_ip4(peer), AppData.get_peer_ip6(peer), AppData.get_peer_port(peer), packet)

	def __send_packet(self, ip4_peer: str, ip6_peer: str, port_peer: str, packet: str):
		try:
			sock, version = self.__create_socket()
			if version == 4:
				sock.connect((ip4_peer, port_peer))
			else:
				sock.connect((ip6_peer, port_peer))
			sock.send(packet.encode())
			sock.close()
		except socket.error as e:
			self.log.write_red('Error sending -> ', end='')
			self.log.write(f'{packet}')
			self.log.write_red(f'{e}')
			return

		self.log.write_blue('Sending -> ', end='')
		self.log.write(f'{packet}')

	def serve(self, sd: socket.socket):
		""" Handle the neighbours requests
		:param sd: the socket descriptor used for read the request
		:return: None
		"""

		try:
			request = sd.recv(200).decode()
		except OSError as e:
			self.log.write_red(f'Unable to read the request from the socket: {e}')
			return

		# log the request received
		socket_ip_sender = sd.getpeername()[0]
		socket_port_sender = sd.getpeername()[1]
		self.log.write_green(f'{socket_ip_sender} [{socket_port_sender}] -> ', end='')
		self.log.write(f'{request}')

		command = request[:4]

		if command == "QUER":
			if len(request) != 102:
				self.log.write_red('Invalid request. Unable to reply.')
				sd.close()
				return

			pktid = request[4:20]
			ip_peer = request[20:75]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = request[75:80]
			ttl = request[80:82]
			query = request[82:102].ljust().rjust().lower()
			sd.close()

			# packet management
			if not AppData.exist_in_received_packets(pktid):
				AppData.add_received_packet(pktid, ip_peer, port_peer)
				t = Timer(300, function=self.__delete_packet, args=(pktid,))
				t.start()
			else:
				return

			# search for the requested file
			results = AppData.search_in_shared_files(query)

			for file in results:
				response = 'AQUE' +\
						pktid + ip_peer + port_peer +\
						AppData.get_shared_filemd5(file) +\
						AppData.get_shared_filename(file).ljust(100)
				self.__send_packet(ip4_peer, ip6_peer, port_peer, response)

			# forwarding the packet to other peers
			self.__forward_packet(socket_ip_sender, ttl, request)

		elif command == "NEAR":
			if len(request) != 82:
				self.log.write_red('Invalid request. Unable to reply.')
				sd.close()
				return

			pktid = request[4:20]
			ip_peer = request[20:75]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = request[75:80]
			ttl = request[80:82]
			sd.close()

			# packet management
			if not AppData.exist_in_received_packets(pktid):
				AppData.add_received_packet(pktid, ip_peer, port_peer)
				t = Timer(300, function=self.__delete_packet, args=(pktid,))
				t.start()
			else:
				return

			# send the NEAR acknowledge
			response = 'ANEA' + pktid + net_utils.get_local_ip_for_response() + net_utils.get_neighbours_port()
			self.__send_packet(ip4_peer, ip6_peer, port_peer, response)

			# forwarding the packet to other peers
			self.__forward_packet(socket_ip_sender, ttl, request)

		elif command == "RETR":
			if len(request) != 36:
				self.log.write_blue('Sending -> ', end='')
				self.log.write('Invalid request. Unable to reply.')
				sd.send('Invalid request. Unable to reply.')
				sd.close()
				return

			file_md5 = request[4:36].decode()

			file_name = AppData.get_shared_filename_by_filemd5(file_md5)

			if file_name is None:
				self.log.write_blue('Sending -> ', end='')
				self.log.write('Sorry, the requested file is not available anymore by the selected peer.')
				sd.send('Sorry, the requested file is not available anymore by the selected peer.')
				sd.close()
				return

			try:
				fd = os.open('shared/' + file_name, os.O_RDONLY)
			except OSError as e:
				self.log.write_blue('Sending -> ', end='')
				self.log.write('Sorry, the peer encountered a problem while serving your request.')
				sd.send('Sorry, the peer encountered a problem while serving your request.')
				sd.close()
				return

			Uploader(sd, fd).start()
		else:
			self.log.write_red('Invalid request. Unable to reply.')
			sd.close()

		return
