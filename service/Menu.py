#!/usr/bin/env python

from handler.MenuHandler import MenuHandler
from utils import net_utils
from utils import shell_colors
from service.AppData import AppData


class Menu:

	def __init__(self, handler: MenuHandler):
		self.handler = handler

	def show(self) -> None:
		""" Shows the menu that interacts with the user

		:return: None
		"""

		choice = ''
		while choice != 'q':
			print('\n- Main Menù -----------------------')
			print('| <1> Search a file to download   |')
			print('| <2> Search all peers around you |')
			print('| <3> List peers                  |')
			print('| <4> Add a peer                  |')
			print('| <5> Remove a peer               |')
			print('-----------------------------------')
			choice = input('Select an option (q to exit): ')

			if choice in {'1', '2', '3', '4', '5'}:
				if len(AppData.get_neighbours()) == 0:
					shell_colors.print_red('\n! You need to have at least one peer to get started !\n')
					command = 'ADDPEER'
				elif choice == '1':
					command = 'QUER'
				elif choice == '2':
					command = 'NEAR'
				elif choice == '3':
					command = 'LISTPEERS'
				elif choice == '4':
					command = 'ADDPEER'
				elif choice == '5':
					command = 'REMOVEPEER'

				self.handler.serve(command)
			elif choice != 'q':
				shell_colors.print_red('Input code is wrong. Choose one action!\n')

		shell_colors.print_blue('\nBye!\n')
