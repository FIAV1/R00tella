#!/usr/bin/env python

from service.Server import Server
from service.Menu import Menu
from handler.NeighboursHandler import NeighboursHandler
from handler.MenuHandler import MenuHandler
from utils import shell_colors as shell
from multiprocessing import Process
import os


if __name__ == '__main__':

	shell.print_orange(' ____   ___   ___  _       _ _       ')
	shell.print_red('|  _ \ / _ \ / _ \| |_ ___| | | __ _ ')
	shell.print_yellow('| |_) | | | | | | | __/ _ \ | |/ _` |')
	shell.print_green('|  _ <| |_| | |_| | ||  __/ | | (_| |')
	shell.print_blue('|_| \__\\___/ \___/ \__\___|_|_|\__,_|')

	if not os.path.exists('shared'):
		os.mkdir('shared')
	if not os.path.exists('downloads'):
		os.mkdir('downloads')

	p = Process(target=lambda: Server(3000, NeighboursHandler()).run())
	p.daemon = True
	p.start()

	Menu(MenuHandler()).show()
