#!/usr/bin/env python


class HandlerInterface:

	def serve(self, request: bytes) -> str:
		pass
