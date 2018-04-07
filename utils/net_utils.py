#!/usr/bin/env python

import re
import ipaddress
from service.AppData import AppData
from utils import shell_colors

config = {
	'ipv4': '172.16.1.1',
	'ipv6': 'fcb0::1:1',
	'neighbours_port': 3000,
	'aque_port': 4000,
	'anea_port': 5000
}


def get_ip_pair(ip_string: str) -> tuple:
	"""
	- Il backslash (\) definisce che il prossimo carattere va interpretato come meta carattere,
	diversamente da come lo si interpreta di solito;
	infatti il punto che segue normalmente vorrebbe dire “un carattere qualsiasi”,
	ma in questo caso significa “un punto”.

	- Le parentesi quadre vengono utilizzate per definire un set di caratteri
	e si può utilizzare in due modi: [XY] oppure [0-9].
	Qualsiasi carattere compreso nelle parentesi può essere confrontato.

	-  L’asterisco ci dice “zero o più di quello che mi precede”.
	Ad esempio la RegEx abc* filtra “ab”, “abc”, “abcc”, e tutto ciò che segue come “abccccccc”.

	:param ip_string: the ip address
	:return: a tuple composed by ipv4 and ipv6
	"""
	ip_v4 = re.sub('\.[0]{1,2}', '.', ip_string[:15])
	ip_v6 = ipaddress.IPv6Address(ip_string[16:]).compressed
	return ip_v4, ip_v6


def get_local_ip_for_response() -> str:
	ipv4 = config['ipv4'].split('.')[0].zfill(3)
	for i in range(1, 4):
		ipv4 = ipv4 + '.' + config['ipv4'].split('.')[i].zfill(3)

	return ipv4 + '|' + ipaddress.IPv6Address(config['ipv6']).exploded


def get_local_ipv4() -> str:
	return config['ipv4']


def set_local_ipv4(ipv4: str) -> str:
	config['ipv4'] = ipv4


def get_local_ipv6() -> str:
	return config['ipv6']


def set_local_ipv6(ipv6: str) -> str:
	config['ipv6'] = ipv6


def get_neighbours_port() -> int:
	return config['neighbours_port']


def get_aque_port() -> int:
	return config['aque_port']


def get_anea_port() -> int:
	return config['anea_port']


def prompt_parameters_request() -> None:
	""" Guide the user to insert his local ip adresses and port in case there are not/they are wrong

	:return: None
	"""
	if '' in (config['ipv4'], config['ipv6']):
		shell_colors.print_blue('\nYou need to add your own network configuration to get started.\n')

	while True:
		if get_local_ipv4() == '':
			ip4 = input('Insert your local IPv4 address: ')
			try:
				ipaddress.IPv4Address(ip4)
			except ipaddress.AddressValueError:
				shell_colors.print_red(f'\n{ip4} is not a valid IPv4 address, please retry.\n')
				continue
			set_local_ipv4(ip4)
			break
		else:
			try:
				ipaddress.IPv4Address(get_local_ipv4())
				break
			except ipaddress.AddressValueError:
				shell_colors.print_red(f'\n{get_local_ipv4()} is not a valid IPv4 address, please reinsert it.\n')
				continue

	while True:
		if get_local_ipv6() == '':
			ip6 = input('Insert your local IPv6 address: ')
			try:
				ipaddress.IPv6Address(ip6)
			except ipaddress.AddressValueError:
				shell_colors.print_red(f'\n{ip6} is not a valid IPv6 address, please retry.\n')
				continue
			set_local_ipv6(ip6)
			break
		else:
			try:
				ipaddress.IPv6Address(get_local_ipv6())
				break
			except ipaddress.AddressValueError as e:
				shell_colors.print_red(f'\n{get_local_ipv6()} is not a valid IPv6 address, please reinsert it.\n')
				continue


def prompt_neighbours_request() -> None:
	""" Guide the user to manually insert peers in the data structure

	:return: None
	"""
	shell_colors.print_blue(
		'\nThis process will allow you to add new peers to your list of known peers (enter "q" to exit).\n')

	while True:
		while True:
			ip4 = input('Insert a known peer (IPv4): ')
			if ip4 == 'q':
				break

			try:
				ipaddress.IPv4Address(ip4)
			except ipaddress.AddressValueError:
				shell_colors.print_red(f'{ip4} is not a valid IPv4 address, please retry.')
				continue
			break

		if ip4 == 'q':
			break

		while True:
			ip6 = input('Insert a known peer (IPv6): ')
			try:
				ipaddress.IPv6Address(ip6)
			except ipaddress.AddressValueError:
				shell_colors.print_red(f'{ip6} is not a valid IPv6 address, please retry.')
				continue
			break

		if ip6 == 'q':
			break

		while True:
			port = input('Insert a known peer (port): ')
			try:
				if port == 'q':
					break

				port = int(port)
				if not 1024 < port < 65535:
					shell_colors.print_red(f'{port} must be in range 1025 - 65535')
					continue
			except ValueError:
				shell_colors.print_red(f'{port} is not a valid port number, please retry.')
				continue
			break

		if port == 'q':
			break

		AppData.add_neighbour(ip4, ip6, port)

		shell_colors.print_green(f'\nSuccessfully added the new peer: {ip4}|{ip6} [{port}]\n')
