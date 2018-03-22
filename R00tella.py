#!/usr/bin/env python

from service.Server import Server
from service.Downloader import Downloader
from utils import shell_colors as shell
import multiprocessing


def server():
	Server(3000).run()


if __name__ == '__main__':

	shell.print_orange(' ____   ___   ___  _       _ _       ')
	shell.print_red('|  _ \ / _ \ / _ \| |_ ___| | | __ _ ')
	shell.print_yellow('| |_) | | | | | | | __/ _ \ | |/ _` |')
	shell.print_green('|  _ <| |_| | |_| | ||  __/ | | (_| |')
	shell.print_blue('|_| \__\\___/ \___/ \__\___|_|_|\__,_|')

	p = multiprocessing.Process(target=server)
	p.daemon = True
	p.start()
