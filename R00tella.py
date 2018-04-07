#!/usr/bin/env python

from service.Server import Server
from service.Menu import Menu
from handler.NeighboursHandler import NeighboursHandler
from handler.MenuHandler import MenuHandler
from utils import shell_colors as shell
from threading import Thread
import os
from utils import net_utils, Logger, hasher
from service.AppData import AppData

if __name__ == '__main__':

	shell.print_orange(' ____   ___   ___  _       _ _       ')
	shell.print_red('|  _ \ / _ \ / _ \| |_ ___| | | __ _ ')
	shell.print_yellow('| |_) | | | | | | | __/ _ \ | |/ _` |')
	shell.print_green('|  _ <| |_| | |_| | ||  __/ | | (_| |')
	shell.print_blue('|_| \__\\___/ \___/ \__\___|_|_|\__,_|')

	if not os.path.exists('shared'):
		os.mkdir('shared')

	for dir_entry in os.scandir('shared'):
		AppData.add_shared_file(dir_entry.name, hasher.get_md5(dir_entry.path), dir_entry.stat().st_size)

	net_utils.prompt_parameters_request()

	# for testing fast
	AppData.add_neighbour('192.168.1.78', 'fc00::1:2', 3000)

	while len(AppData.get_neighbours()) == 0:
		net_utils.prompt_neighbours_request()

	log = Logger.Logger('neighbours.log')

	t = Thread(target=lambda: Server(net_utils.get_neighbours_port(), NeighboursHandler(log)).run(False))
	t.daemon = True
	t.start()

	Menu(MenuHandler()).show()
