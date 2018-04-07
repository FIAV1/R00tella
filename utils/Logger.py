#!/usr/bin/env python

from utils import shell_colors as colors


class Logger:
	""" Utils class used to write into a logger with colors (useful for debug purposes) """

	def __init__(self, filename: str):
		self.filename = filename
		log = open(self.filename, 'w')
		log.close()

	def write(self, string: str, end='\n'):
		log = open(self.filename, 'at+')
		log.write(string + end)
		log.close()

	def write_red(self, string: str, end='\n'):
		log = open(self.filename, 'at+')
		log.write(colors.DEFAULTBG + colors.BOLD + colors.RED + string + colors.RESET + end)
		log.close()

	def write_blue(self, string: str, end='\n'):
		log = open(self.filename, 'at+')
		log.write(colors.DEFAULTBG + colors.BOLD + colors.BLUE + string + colors.RESET + end)
		log.close()

	def write_green(self, string: str, end='\n'):
		log = open(self.filename, 'at+')
		log.write(colors.DEFAULTBG + colors.BOLD + colors.GREEN + string + colors.RESET + end)
		log.close()

	def write_yellow(self, string: str, end='\n'):
		log = open(self.filename, 'at+')
		log.write(colors.DEFAULTBG + colors.BOLD + colors.YELLOW + string + colors.RESET + end)
		log.close()

	def write_orange(self, string: str, end='\n'):
		log = open(self.filename, 'at+')
		log.write(colors.DEFAULTBG + colors.BOLD + colors.ORANGE + string + colors.RESET + end)
		log.close()
