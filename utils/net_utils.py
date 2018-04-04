#!/usr/bin/env python

import re
import ipaddress

config = {
	'ipv4': '172.16.1.1',
	'ipv6': 'fc00::1:1',
	'neighbours_port': '3000',
	'aque_port': '4000',
	'anea_port': '5000'
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
	"""
	ip_v4 = re.sub('\.[0]*', '.', ip_string[:15])
	ip_v6 = ipaddress.IPv6Address(ip_string[16:]).compressed
	return ip_v4, ip_v6


def get_local_ip_for_response():
	ipv4 = config['ipv4'].split('.')[0].zfill(3)
	for i in range(1, 4):
		ipv4 = ipv4 + '.' + config['ipv4'].split('.')[i].zfill(3)

	return ipv4 + '|' + ipaddress.IPv6Address(config['ipv6']).exploded


def get_local_ipv4():
	return config['ipv4']


def set_local_ipv4(ipv4: str):
	config['ipv4'] = ipv4


def get_local_ipv6():
	return config['ipv6']


def set_local_ipv6(ipv6: str):
	config['ipv6'] = ipv6


def get_neighbours_port():
	return config['neighbours_port']


def get_aque_port():
	return config['aque_port']


def get_anea_port():
	return config['anea_port']


def prompt_parameters_request():
	while True:
		if get_local_ipv4() == '':
			ip4 = input('Insert your local IPv4 address: ')
			try:
				ipaddress.IPv4Address(ip4)
			except ipaddress.AddressValueError as e:
				print(f'{ip4} is not a valid IPv4 address, please retry.')
				continue
			set_local_ipv4(ip4)
			break
		else:
			try:
				ipaddress.IPv4Address(get_local_ipv4())
				break
			except ipaddress.AddressValueError as e:
				ip4 = input(f'{get_local_ipv4()} is not a valid IPv4 address, please reinsert it: ')
				set_local_ipv4(ip4)
				continue

	while True:
		if get_local_ipv6() == '':
			ip6 = input('Insert your local IPv6 address: ')
			try:
				ipaddress.IPv6Address(ip6)
			except ipaddress.AddressValueError as e:
				print(f'{ip6} is not a valid IPv6 address, please retry.')
				continue
			set_local_ipv6(ip6)
			break
		else:
			try:
				ipaddress.IPv6Address(get_local_ipv6())
				break
			except ipaddress.AddressValueError as e:
				ip6 = input(f'{get_local_ipv6()} is not a valid IPv6 address, please reinsert it: ')
				set_local_ipv6(ip6)
				continue
