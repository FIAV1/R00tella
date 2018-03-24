#!/usr/bin/env python

import socket


class HandlerInterface:

	def serve(self, request: str, sd: socket.socket) -> None:
		pass
