"""Common constants and functions"""
from sys import version_info
from os import name, system
from os import path, makedirs
import pickle

from house import House


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


def saveData(print_log: bool = False) -> None:
	def internalLog(message: str) -> None:
		if print_log:
			print(message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = 'data'
	full_path = path.join(absolute_path, relative_path)
	
	internalLog("Reaching the data folder")
	if not path.isdir(full_path):
		internalLog("No data folder, creating one")
		makedirs(full_path)
		
	internalLog("Writing houses data")
	relative_path = "data/table"
	full_path = path.join(absolute_path, relative_path)
	with open(full_path, 'wb') as file:
		# No need dump House.n_house, just count it later
		pickle.dump(House.table, file)
	
	internalLog("Writing tickets data")
	relative_path = "data/tickets"
	full_path = path.join(absolute_path, relative_path)
	with open(full_path, 'wb') as file:
		pickle.dump([House.total_tickets, House.tickets], file)
	
	internalLog("Data saved")


def loadData(print_log: bool = False) -> None:
	def internalLog(message: str) -> None:
		if print_log:
			print(message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = "data/table"
	full_path = path.join(absolute_path, relative_path)
	try:
		internalLog("Finding houses data")
		with open(full_path, 'rb') as file:
			data: dict = pickle.load(file)
		House.table = data
		House.n_House = len(House.table)
		internalLog("Houses data loaded")
	except FileNotFoundError:
		internalLog("No houses data found")
	
	
	relative_path = "data/tickets"
	full_path = path.join(absolute_path, relative_path)
	try:
		internalLog("Finding tickets data")
		with open(full_path, 'rb') as file:
			data: dict = pickle.load(file)
		House.total_tickets = data[0]
		House.tickets = data[1]
		internalLog("Tickets data loaded")
	except FileNotFoundError:
		internalLog("No tickets data found")
	
	
	internalLog("Data loaded")

