#!/usr/bin/env python

from handler.MenuHandler import MenuHandler


class Menu:

	def __init__(self, handler: MenuHandler):
		self.handler = handler

	def show(self) -> None:

		choice = ''
		while choice != 'q':

			choice = input('Select an option (q to exit):\n1] Search a file to download\n2] Search all Peers around you\n')

			if choice in {'1', '2'}:
				if choice == '1':
					command = 'QUER'
				elif choice == '2':
					command = 'NEAR'

				self.handler.serve(command)
			elif choice != 'q':
				print('Input code is wrong. Choose one action!\n\n')

		print('\nBye!\n')
