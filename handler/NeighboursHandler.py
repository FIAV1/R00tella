#!/usr/bin/env python

import socket
import random
from handler.HandlerInterface import HandlerInterface
from service.AppData import AppData
from service.Uploader import Uploader
from utils import net_utils, Logger
from threading import Timer
import os
import ipaddress


class NeighboursHandler(HandlerInterface):

	def __init__(self, log: Logger.Logger):
		self.log = log

	def __delete_packet(self, pktid: str) -> None:
		""" Delete a packet from the net

		:param pktid: id of the packet
		:return: None
		"""
		if AppData.exist_in_received_packets(pktid):
			AppData.delete_received_packet(pktid)

	def __create_socket(self) -> (socket.socket, int):
		""" Create the active socket

			:return: the active socket and the version
		"""
		if random.random() <= 0.5:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(2)
			version = 4
		else:
			sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			sock.settimeout(2)
			version = 6

		return sock, version

	def __forward_packet(self, ip_sender: str, ip_source: str, ttl: str, packet: str) -> None:
		""" Forward a packet in the net to neighbours

		:param ip_sender: ip address of sender host
		:param ttl: packet time to live
		:param packet: string representing the packet
		:return: None
		"""
		new_ttl = int(ttl) - 1

		if new_ttl > 0:
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_source)

			# get the recipients list without the peer who sent the packet
			recipients = AppData.get_neighbours_recipients(ip_sender, ip4_peer, ip6_peer)

			packet = packet[:80] + str(new_ttl).zfill(2) + packet[82:]

			for peer in recipients:
				self.__unicast(AppData.get_peer_ip4(peer), AppData.get_peer_ip6(peer), AppData.get_peer_port(peer), packet)

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
			self.log.write_red(f'Error sending {ip4_peer}|{ip6_peer} [{port_peer}] -> ', end='')
			self.log.write(f'{packet}')
			self.log.write_red(f'{e}')
			return

		self.log.write_blue(f'Sending {ip4_peer}|{ip6_peer} [{port_peer}] -> ', end='')
		self.log.write(f'{packet}')

	def serve(self, sd: socket.socket) -> None:
		""" Handle the neighbours packet

		:param sd: the socket descriptor used for read the packet
		:return: None
		"""

		try:
			packet = sd.recv(200).decode()
		except socket.error as e:
			self.log.write_red(f'Unable to read the packet from the socket: {e}')
			sd.close()
			return

		# log the packet received
		socket_ip_sender = sd.getpeername()[0]
		if ipaddress.IPv6Address(socket_ip_sender).ipv4_mapped is None:
			socket_ip_sender = ipaddress.IPv6Address(socket_ip_sender).compressed
		else:
			socket_ip_sender = ipaddress.IPv6Address(socket_ip_sender).ipv4_mapped.compressed

		socket_port_sender = sd.getpeername()[1]
		self.log.write_green(f'{socket_ip_sender} [{socket_port_sender}] -> ', end='')
		self.log.write(f'{packet}')

		command = packet[:4]

		if command == "QUER":
			if len(packet) != 102:
				self.log.write_red('Invalid packet. Unable to reply.')
				sd.close()
				return

			pktid = packet[4:20]
			ip_peer = packet[20:75]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = int(packet[75:80])
			ttl = packet[80:82]
			query = packet[82:102].lstrip().rstrip().lower()
			sd.close()

			# packet management
			if pktid == AppData.get_sent_packet():
				return

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
						pktid + net_utils.get_local_ip_for_response() +\
						str(net_utils.get_neighbours_port()).zfill(5) +\
						AppData.get_shared_filemd5(file) +\
						AppData.get_shared_filename(file).ljust(100)
				self.__unicast(ip4_peer, ip6_peer, port_peer, response)

			# forwarding the packet to other peers
			self.__forward_packet(socket_ip_sender, ip_peer, ttl, packet)

		elif command == "NEAR":
			if len(packet) != 82:
				self.log.write_red('Invalid packet. Unable to reply.')
				sd.close()
				return

			pktid = packet[4:20]
			ip_peer = packet[20:75]
			ip4_peer, ip6_peer = net_utils.get_ip_pair(ip_peer)
			port_peer = int(packet[75:80])
			ttl = packet[80:82]
			sd.close()

			# packet management
			if pktid == AppData.get_sent_packet():
				return

			if not AppData.exist_in_received_packets(pktid):
				AppData.add_received_packet(pktid, ip_peer, port_peer)
				t = Timer(300, function=self.__delete_packet, args=(pktid,))
				t.start()
			else:
				return

			# send the NEAR acknowledge
			response = 'ANEA' + pktid + net_utils.get_local_ip_for_response() + str(net_utils.get_neighbours_port()).zfill(5)
			self.__unicast(ip4_peer, ip6_peer, port_peer, response)

			# forwarding the packet to other peers
			self.__forward_packet(socket_ip_sender, ip_peer, ttl, packet)

		elif command == "RETR":
			if len(packet) != 36:
				self.log.write_blue('Sending -> ', end='')
				self.log.write('Invalid packet. Unable to reply.')
				sd.send('Invalid packet. Unable to reply.'.encode())
				sd.close()
				return

			file_md5 = packet[4:36]

			file_name = AppData.get_shared_filename_by_filemd5(file_md5)

			if file_name is None:
				self.log.write_blue('Sending -> ', end='')
				self.log.write('Sorry, the requested file is not available anymore by the selected peer.')
				sd.send('Sorry, the requested file is not available anymore by the selected peer.'.encode())
				sd.close()
				return

			try:
				f_obj = open('shared/' + file_name, 'rb')
			except OSError as e:
				self.log.write_red(f'Cannot open the file to upload: {e}')
				self.log.write_blue('Sending -> ', end='')
				self.log.write('Sorry, the peer encountered a problem while serving your packet.')
				sd.send('Sorry, the peer encountered a problem while serving your packet.'.encode())
				sd.close()
				return

			try:
				Uploader(sd, f_obj, self.log).start()
				self.log.write_blue(f'Sent {sd.getpeername()[0]} [{sd.getpeername()[1]}] -> ', end='')
				self.log.write(f'{file_name}')
				sd.close()
			except OSError:
				self.log.write_red('Error while sending the file.')
				sd.close()
				return

		else:
			self.log.write_red('Invalid packet. Unable to reply.')
			sd.close()

		return
