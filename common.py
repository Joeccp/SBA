"""Common constants and functions"""
import string
from sys import version_info
from os import name, system


def clearScreen() -> None:
	"""
	Clear the screen

	It checks which platform is it running on,
	then executes the command for clearing the screen.

	May not work on Thonny or other IDE
	"""
	if name == 'nt':  # Windows
		system('cls')
	elif name == 'posix':  # Mac / Linux
		system('clear')
	else:  # Skip a few lines instead
		print("\n\n\n\n\n\n", end='')


def checkPythonVersion() -> None:
	"""
	Checks the Python version.
	If the python version is older than 3.11, it raises an exception.
	:return: None
	:raises SystemExit: If Python version is older than 3.11
	"""
	major_version, minor_version, *_ = version_info
	if major_version < 3:
		err_msg: str = "This program does not support Python 2"
		raise SystemExit(err_msg)
	elif minor_version < 11:
		err_msg: str = "Unsupported old Python version, please use Python 3.11 or newer"
		raise SystemExit(err_msg)
