#!/usr/bin/env python

from .Menu import Menu


class Peer:

	def __init__(self, port: int, menu: Menu):
		self.menu = menu
		self.port = port
		self.sd = None # sd è il descriptor della socket che il peer usa per mandare request

	def __create_socket(self):
		pass

	def run(self):

		while True:
			self.__create_socket()
			self.menu.run(self.sd)
