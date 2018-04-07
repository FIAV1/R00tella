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
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))

    filled_length = int(length * iteration // total)

    bar = fill * filled_length + '-' * (length - filled_length)

    shell_colors.print_blue('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')

    # Print New Line on Complete
    if iteration == total:
        print()
