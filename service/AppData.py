#!/usr/bin/env python

import re


class AppData:

	# ('filename', 'md5', 'dim')
	shared_files = list()

	# {'pktid' : (ip, port)}
	packets = dict()

	# ('ipv4', 'ipv6', 'port)
	neighbours = list()

	peer_files = list()

	# received packet management --------------------------------------------------
	@classmethod
	def add_packet(cls, pktid: str, ip_peer: str, port_peer: str) -> None:
		cls.packets[pktid] = (ip_peer, port_peer)

	@classmethod
	def exist_packet(cls, pktid: str) -> bool:
		return pktid in cls.packets
	# -----------------------------------------------------------------------------

	# shared files management -----------------------------------------------------
	@classmethod
	def search_in_shared_files(cls, query_name: str) -> list:
		results = list()
		for file in cls.shared_files:
			if re.search(query_name, file[0]):
				results.append(file)
		return results

	@classmethod
	def get_shared_filename(cls, file: tuple) -> str:
		return file[0]

	@classmethod
	def get_shared_filemd5(cls, file: tuple) -> str:
		return file[1]
	# -----------------------------------------------------------------------------

	# peer list management --------------------------------------------------------
	@classmethod
	def is_neighbour(cls, peer: tuple) -> bool:
		return peer in cls.neighbours

	@classmethod
	def get_peer_ip4(cls, peer: tuple) -> str:
		return peer[0]

	@classmethod
	def get_peer_ip6(cls, peer: tuple) -> str:
		return peer[1]

	@classmethod
	def get_peer_port(cls, peer: tuple) -> str:
		return peer[2]
	# -----------------------------------------------------------------------------