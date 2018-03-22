import sqlite3
from sqlite3 import Error
from sqlite3 import DatabaseError
import os.path


def exist(db_filename: str) -> bool:
	""" Check if the given db exist

	Parameters:
		db_filename: the db filename
	Returns:
		bool - True or False either if exists or not
	"""
	if os.path.exists(db_filename):
		return True
	return False


def create_database(db_filename: str) -> None:
	""" Create a sqlite db file with the structure defined in the 'schema.sql' file

	Parameters:
		db_filename: the db filename
	"""
	try:
		db_file = open(db_filename, "w+")
		sqlscript = open('database/schema.sql', 'r')
	except IOError as e:
		print(e)
		exit(0)

	if db_file is not None and sqlscript is not None:

		# create a database connection
		conn = get_connection(db_filename)

		try:
			# create files table
			conn.executescript(sqlscript.read())
			# commits the statements
			conn.commit()
			# close the database
			conn.close()
		except Error as e:
			conn.rollback()
			conn.close()
			print(e)
			exit(0)

	else:
		print("Error: cannot create the database file.")


def reset_database(db_filename: str) -> bool:
	""" Refresh the tables of the database

	Parameters:
		db_filename: the db filename
	Returns:
		bool - True or False either if succeeds or fails
	"""
	try:
		sqlscript = open('database/reset.sql', 'r')
	except IOError as e:
		print(e)
		exit(0)
	# create a database connection
	conn = get_connection(db_filename)

	try:
		# delete all tables content
		conn.executescript(sqlscript.read())
		# commits the statement
		conn.commit()
		# close the database
		conn.close()
		return True
	except Error as e:
		conn.rollback()
		conn.close()
		print(e)
		exit(0)
		return False


def fill_seeds(db_filename: str) -> bool:

	try:
		reset_script = open('database/reset.sql', 'r')
		# seeds_script = open('database/seeds.sql', 'r')
	except IOError as e:
		print(e)
		exit(0)
	# create a database connection
	conn = get_connection(db_filename)

	try:
		conn.executescript(reset_script.read())
		# conn.executescript(seeds_script.read())
		# commits the statement
		conn.commit()
		# close the database
		conn.close()
		return True
	except Error as e:
		conn.rollback()
		conn.close()
		print(e)
		exit(0)
		return False


def get_connection(db_filename: str) -> sqlite3.Connection:
	""" create a database connection to the given SQLite database

	Parameters:
		db_filename: the db filename
	Returns:
		Connection - Connection object or None
	"""
	try:
		return sqlite3.connect(db_filename)

	except Error as e:
		raise e

