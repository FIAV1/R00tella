#!/usr/bin/env python

import socket


class HandlerInterface:

	def serve(self, sd: socket.socket) -> None:
		""" Handlers interface

		:param sd: socket descriptor
		:return: None
		"""
		pass
