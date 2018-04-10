#!/usr/bin/env python

import re


class AppData:
	""" Data class containing data structures and methods to interact with them """

	# ('filename', 'md5', 'dim')
	shared_files = list()

	# {'pktid' : (ip, port)}
	received_packets = dict()

	# ('ipv4', 'ipv6', 'port')
	neighbours = list()

	# ('ipv4', 'ipv6', 'port', 'md5', 'filename')
	peer_files = list()

	# 'pktid'
	sent_packet = str()

	# received packets management --------------------------------------------------
	@classmethod
	def add_received_packet(cls, pktid: str, ip_peer: str, port_peer: int) -> None:
		cls.received_packets[pktid] = (ip_peer, port_peer)

	@classmethod
	def delete_received_packet(cls, pktid: str) -> None:
		del cls.received_packets[pktid]

	@classmethod
	def exist_in_received_packets(cls, pktid: str) -> bool:
		return pktid in cls.received_packets
	# -----------------------------------------------------------------------------

	# shared files management -----------------------------------------------------
	@classmethod
	def add_shared_file(cls, filename: str, file_md5: str, file_size: int) -> None:
		cls.shared_files.append((filename, file_md5, file_size))

	@classmethod
	def search_in_shared_files(cls, query_name: str) -> list:
		results = list()
		for file in cls.shared_files:
			if re.search(query_name, file[0].lower()):
				results.append(file)
		return results

	@classmethod
	def get_shared_filename_by_filemd5(cls, file_md5: str) -> str:
		for file in cls.shared_files:
			if file[1] == file_md5:
				return file[0]

	@classmethod
	def get_shared_filename(cls, file: tuple) -> str:
		return file[0]

	@classmethod
	def get_shared_filemd5(cls, file: tuple) -> str:
		return file[1]

	@classmethod
	def get_filename_by_filemd5_on_shared_files(cls, file_md5: str) -> str:
		for file in cls.shared_files:
			if file[1] == file_md5:
				return file[0]
	# -----------------------------------------------------------------------------

	# neighbours management --------------------------------------------------------
	@classmethod
	def is_neighbour(cls, ip4_peer: str, ip6_peer: str, port_peer: int) -> bool:
		return (ip4_peer, ip6_peer, port_peer) in cls.neighbours

	@classmethod
	def get_neighbours(cls) -> list:
		return cls.neighbours

	@classmethod
	def add_neighbour(cls, ip4_peer: str, ip6_peer: str, port_peer: int) -> None:
		cls.neighbours.append((ip4_peer, ip6_peer, port_peer))

	@classmethod
	def neighbour_index(cls, ip4_peer: str, ip6_peer: str, port_peer: int) -> int:
		return cls.neighbours.index((ip4_peer, ip6_peer, port_peer))

	@classmethod
	def get_neighbours_recipients(cls, ip_sender: str, ip4_source: str, ip6_source: str) -> list:
		recipients = cls.neighbours.copy()

		for peer in cls.neighbours:
			if ip_sender == peer[0] or ip_sender == peer[1]:
				recipients.remove(peer)

			elif ip4_source == peer[0] or ip6_source == peer[1]:
				recipients.remove(peer)

		return recipients

	@classmethod
	def get_peer_ip4(cls, peer: tuple) -> str:
		return peer[0]

	@classmethod
	def get_peer_ip6(cls, peer: tuple) -> str:
		return peer[1]

	@classmethod
	def get_peer_port(cls, peer: tuple) -> int:
		return peer[2]

	@classmethod
	def remove_neighbour(cls, neighbour_index: int) -> None:
		cls.neighbours.pop(neighbour_index)
	# -----------------------------------------------------------------------------

	# peer_files management--------------------------------------------------------
	@classmethod
	def get_peer_files(cls) -> list:
		return cls.peer_files

	@classmethod
	def get_file_owner_ip4(cls, file: tuple) -> str:
		return file[0]

	@classmethod
	def get_file_owner_ip6(cls, file: tuple) -> str:
		return file[1]

	@classmethod
	def get_file_owner_port(cls, file: tuple) -> int:
		return file[2]

	@classmethod
	def get_file_md5(cls, file: tuple) -> str:
		return file[3]

	@classmethod
	def get_file_name(cls, file: tuple) -> str:
		return file[4]

	@classmethod
	def add_peer_files(cls, ip4_peer: str, ip6_peer: str, port_peer: int, filemd5: str, filename: str) -> None:
		cls.peer_files.append((ip4_peer, ip6_peer, port_peer, filemd5, filename))

	@classmethod
	def exist_peer_files(cls, ip4_peer: str, ip6_peer: str, port_peer: int, filemd5: str, filename: str) -> bool:
		return (ip4_peer, ip6_peer, port_peer, filemd5, filename) in cls.peer_files

	@classmethod
	def peer_file_index(cls, ip4_peer: str, ip6_peer: str, port_peer: int, filemd5: str, filename: str) -> int:
		return cls.peer_files.index((ip4_peer, ip6_peer, port_peer, filemd5, filename))

	@classmethod
	def get_peer_file_by_index(cls, index: int) -> tuple:
		return cls.peer_files.pop(index)

	@classmethod
	def clear_peer_files(cls) -> None:
		cls.peer_files.clear()
	# -----------------------------------------------------------------------------

	# query management-------------------------------------------------------------
	@classmethod
	def set_sent_packet(cls, pktid: str) -> None:
		cls.sent_packet = pktid

	@classmethod
	def get_sent_packet(cls) -> str:
		return cls.sent_packet
	# -----------------------------------------------------------------------------
