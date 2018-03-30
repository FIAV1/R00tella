#!/usr/bin/env python

from service.Server import Server
from service.Menu import Menu
from handler.NeighboursHandler import NeighboursHandler
from handler.MenuHandler import MenuHandler
from utils import shell_colors as shell
from threading import Thread
import os
from utils import net_utils, Logger
import ipaddress

if __name__ == '__main__':

	shell.print_orange(' ____   ___   ___  _       _ _       ')
	shell.print_red('|  _ \ / _ \ / _ \| |_ ___| | | __ _ ')
	shell.print_yellow('| |_) | | | | | | | __/ _ \ | |/ _` |')
	shell.print_green('|  _ <| |_| | |_| | ||  __/ | | (_| |')
	shell.print_blue('|_| \__\\___/ \___/ \__\___|_|_|\__,_|')

	if not os.path.exists('shared'):
		os.mkdir('shared')

	while True:
		if net_utils.get_local_ipv4() == '':
			ip4 = input('Insert your local IPv4 address: ')
			try:
				ipaddress.IPv4Address(ip4)
			except ipaddress.AddressValueError as e:
				print(f'{ip4} is not a valid IPv4 address, please retry.')
				continue
			net_utils.set_local_ipv4(ip4)
			break
		else:
			try:
				ipaddress.IPv4Address(net_utils.get_local_ipv4())
				break
			except ipaddress.AddressValueError as e:
				ip4 = input(f'{net_utils.get_local_ipv4()} is not a valid IPv4 address, please reinsert it:')
				net_utils.set_local_ipv4(ip4)
				continue

	while True:
		if net_utils.get_local_ipv6() == '':
			ip6 = input('Insert your local IPv6 address: ')
			try:
				ipaddress.IPv6Address(ip6)
			except ipaddress.AddressValueError as e:
				print(f'{ip6} is not a valid IPv6 address, please retry.')
				continue
			net_utils.set_local_ipv6(ip6)
			break
		else:
			try:
				ipaddress.IPv6Address(net_utils.get_local_ipv6())
				break
			except ipaddress.AddressValueError as e:
				ip6 = input(f'{net_utils.get_local_ipv6()} is not a valid IPv6 address, please reinsert it:')
				net_utils.set_local_ipv6(ip6)
				continue

	log = Logger.Logger('neighbours.log')

	t = Thread(target=lambda: Server(net_utils.get_neighbours_port(), NeighboursHandler(log)).run())
	t.daemon = True
	t.start()

	Menu(MenuHandler()).show()
