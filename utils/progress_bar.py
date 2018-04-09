from utils import shell_colors


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█') -> None:
	""" Call in a loop to create terminal progress bar

		:param iteration: Required - current iteration (Int)
		:param total: Required - total iterations (Int)
		:param prefix: Optional - prefix string (Str)
		:param suffix: Optional - suffix string (Str)
		:param decimals: Optional - positive number of decimals in percent complete (Int)
		:param length: Optional - character length of bar (Int)
		:param fill: Optional - bar fill character (Str)
		:return: None
	"""

	# Calc the percentage to show
	percent = round(100.0 * (iteration / float(total)), 1)

	# Calc the amount of bar to be filled
	filled_length = int(length * iteration // total)

	# Create the bar string to be showed
	bar = fill * filled_length + '-' * (length - filled_length)

	# Prints the loading bar
	shell_colors.print_blue(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')

	# Print new line on complete
	if iteration == total:
		print()
