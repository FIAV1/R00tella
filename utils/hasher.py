#!/usr/bin/env python

import hashlib


def get_md5(file_path: str) -> str:
	"""
	The iter() function has one mandatory argument and one optional argument,
	and it behaves differently depending on whether one or two arguments are provided.

	1) If only one argument is provided,
		then that argument must be an object that supports the iterator protocol,
		i.e. it must implement the __iter__() method, or the sequence protocol,
		i.e. it must implement the __getitem__() method.

	2) If, on the other hand, the second “sentinel” argument is provided,
		then the first argument must be a callable and the iterator returned by iter(callable, sentinel)
		will behave as follows:
		• When the iterator’s next()  method is called,
			the callable passed in as the first argument will be called.
		• If the value returned from next() is equal to the sentinel, then StopIteration  is raised.

	:param file_path: path of the file to hash
	:return: None
	"""
	m = hashlib.md5()
	with open(file_path, "rb") as f:
		for block in iter(lambda: f.read(4096), b''):
			m.update(block)

	return m.hexdigest()
