#!/usr/bin/env python

from handler.HandlerInterface import HandlerInterface
import socket


class Menu:

	def __init__(self, handler: HandlerInterface):
		self.handler = handler

	def run(self, sd: socket.socket) -> None:

		print('Hi! I\'ll be a supercool menu, trust me!')

		choice = input('Select an option: ')

		self.handler.serve(choice, sd)
