#!/usr/bin/env python

from handler.MenuHandler import MenuHandler


class Menu:

	def __init__(self, handler: MenuHandler):
		self.handler = handler

	def show(self) -> None:

		choice = ''
		while choice != 'q':
			print('<1> Search a file to download')
			print('<2> Search all peers around you')
			choice = input('Select an option (q to exit):')

			if choice in {'1', '2'}:
				if choice == '1':
					command = 'QUER'
				elif choice == '2':
					command = 'NEAR'

				self.handler.serve(command)
			elif choice != 'q':
				print('Input code is wrong. Choose one action!\n')

		print('\nBye!')
