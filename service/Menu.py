#!/usr/bin/env python

from handler.MenuHandler import MenuHandler
from utils.net_utils import prompt_neighbours_request
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
			shell_colors.print_orange('\n-----------------------------------')
			shell_colors.print_orange('| <1> Search a file to download   |')
			shell_colors.print_orange('| <2> Search all peers around you |')
			shell_colors.print_orange('| <3> Add peers manually          |')
			shell_colors.print_orange('-----------------------------------')
			shell_colors.print_orange('Select an option (q to exit):')
			choice = input()

			if choice in {'1', '2'}:
				if len(AppData.get_neighbours()) == 0:
					shell_colors.print_red('\n! You need to have at least one peer to get started !')
					continue
				elif choice == '1':
					command = 'QUER'
				elif choice == '2':
					command = 'NEAR'

				self.handler.serve(command)
			elif choice == '3':
				prompt_neighbours_request()
			elif choice != 'q':
				shell_colors.print_red('Input code is wrong. Choose one action!\n')

		shell_colors.print_blue('\nBye!\n')
