#!/usr/bin/env python

import socket


class HandlerInterface:

	def serve(self, sd: socket.socket) -> None:
		pass
