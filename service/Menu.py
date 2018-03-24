#!/usr/bin/env python

from handler.MenuHandler import MenuHandler


class Menu:

	def __init__(self, handler: MenuHandler):
		self.handler = handler

	def show(self) -> None:

		choice = ''
		while choice != 'q':

			choice = input('Select an option (q to exit):\n1] Query\n2] Near\n3] Download\n')

			if choice in {'1', '2', '3'}:
				self.handler.serve(choice)
			elif choice != 'q':
				print('Input code is wrong. Choose one action!\n\n')

		print('\nBye!\n')
