#!/usr/bin/env python

from handler.MenuHandler import MenuHandler


class Menu:

	def __init__(self, handler: MenuHandler):
		self.handler = handler

	def show(self) -> None:

		choice = ''
		while choice != 'q':  # poi la condizione si sistema ovviamente

			print('Hi! I\'ll be a supercool menu, trust me!')

			choice = input('Select an option (q to exit): ')

			self.handler.serve(choice)

		print('\nBye!\n')
