"""Utilities"""

import pickle
from os import makedirs, name, path, system

from house import House


def clearScreen() -> None:
	"""
	Clear the screen

	It checks which platform is it running on,
	then executes the command for clearing the screen.

	May not work on Thonny or other IDE
	
	:return: None
	"""
	if name == 'nt':  # Windows
		system('cls')
	elif name == 'posix':  # Mac / Linux
		system('clear')
	else:  # Skip a few lines instead
		print("\n\n\n\n\n\n", end='')



def saveData(print_log: bool = False) -> None:
	"""
	Save `House.houses_table` into `data/houses`,
	and save `House.total_tickets` and `House.tickets_table` into `data/tickets`
	
	:param print_log: Whether to print logs, it is for admin mode
	:type print_log: bool
	:return: None
	"""
	def internalLog(message: str) -> None:
		"""
		Print logs if `print_log` is `True`
		
		:param message: Message to print
		:type message: str
		:return: None
		"""
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
	relative_path = "data/houses"
	full_path = path.join(absolute_path, relative_path)
	with open(full_path, 'wb') as file:
		# No need save House.n_house, count it later
		pickle.dump(House.houses_table, file)
	
	internalLog("Writing tickets data")
	relative_path = "data/tickets"
	full_path = path.join(absolute_path, relative_path)
	with open(full_path, 'wb') as file:
		pickle.dump([House.total_tickets, House.tickets_table], file)
	
	internalLog("Data saved")


def loadData(print_log: bool = False) -> None:
	"""
	Load `House.houses_table` from `data/houses`,
	and load `House.total_tickets` and `House.tickets_table` from `data/tickets`

	:param print_log: Whether to print logs, it is for admin mode
	:type print_log: bool
	:return: None
	"""
	def internalLog(message: str) -> None:
		"""
		Print logs if `print_log` is `True`

		:param message: Message to print
		:type message: str
		:return: None
		"""
		if print_log:
			print(message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = "data/houses"
	full_path = path.join(absolute_path, relative_path)
	try:
		internalLog("Finding houses data")
		with open(full_path, 'rb') as file:
			data: dict = pickle.load(file)
		House.houses_table = data
		House.n_House = len(House.houses_table)
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
		House.tickets_table = data[1]
		internalLog("Tickets data loaded")
	except FileNotFoundError:
		internalLog("No tickets data found")
	
	
	internalLog("Data loaded")

