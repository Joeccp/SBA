"""Utilities"""

# Copyright 2023 Joe Chau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pickle import dump, load
from datetime import datetime
from logging import basicConfig, DEBUG, getLogger, Logger
from os import get_terminal_size, makedirs, path, system
from platform import system as systemPlatform
from sys import version_info

from .house import House


def checkSystemPlatform() -> None:
	"""
	Checks whether it is running on Windows,
	if not, raises SystemExit

	:return: None
	:raises SystemExit: If not running on Windows
	"""
	logger: Logger = getLogger("checkSystemPlatform")
	logger.info("Checking system platform")
	if systemPlatform() != 'Windows':
		logger.critical("I am running on Non-Windows system platform!")
		logger.critical("QUITTING THE PROGRAM: Non-windows system platform")
		err_msg: str = "This program can only be executed on Windows"
		raise SystemExit(err_msg)


def checkPythonVersion() -> None:
	"""
	Checks the Python version.
	If the python version is older than 3.11, it raises SystemExit.

	:return: None
	:raises SystemExit: If the Python version is older than 3.11
	"""
	# (tomllib, which is required in src.login.login, was introduced in Python 3.11),
	# (typing.Self, which is required in src.house.House, was also introduced in Python 3.11)
	# (match-case syntax, which is used in House.printPlan, was introduced in Python 3.10)
	
	logger: Logger = getLogger("checkPythonVersion")
	major_version, minor_version, *_ = version_info
	if major_version < 3:
		logger.critical("I am running on Python 2!")
		logger.critical("QUITTING THE PROGRAM: Python version lower than Python 3.11")
		err_msg: str = "This program does not support Python 2"
		raise SystemExit(err_msg)
	elif minor_version < 11:
		logger.critical("I am running on Python 3.%s!", minor_version)
		logger.critical("QUITTING THE PROGRAM: Python version lower than Python 3.11")
		err_msg: str = "Unsupported old Python version (" + str(major_version) + "." + str(
			minor_version) + "), please use Python 3.11 or newer"
		raise SystemExit(err_msg)


def clearScreen() -> None:
	"""
	Clear the screen

	:return: None
	"""

	try:
		terminal_width, terminal_height = get_terminal_size()
		# Print empty lines in case system('cls') does not work
		print('\n' * terminal_height, end='')
	except OSError:
		# OSError: [WinError 6] The handle is invalid
		# Normally due to get_terminal_size()
		# But still need to print empty lines in case system('cls') does not work
		print('\n' * 20)
	finally:
		system('cls')


def saveData(*, print_log: bool = False) -> None:
	"""
	Save `House.houses_table` into `data/houses`,
	and save `House.total_tickets` and `House.tickets_table` into `data/tickets`
	
	:param print_log: Whether to print logs, it is for admin mode. Keyword-only parameter
	:type print_log: bool
	:return: None
	"""
	
	logger: Logger = getLogger('saveData')
	logger.info("Saving Data")
	
	def internalLog(message: str) -> None:
		"""
		Print log if `print_log` is `True`
		
		:param message: Message to print
		:type message: str
		:return: None
		"""
		if print_log:
			print(message)
		logger.info(message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = '../data'
	full_path = path.join(absolute_path, relative_path)
	
	internalLog("Reaching the data folder")
	if not path.isdir(full_path):
		internalLog("No data folder, creating one")
		makedirs(full_path)
	
	internalLog("Writing houses data")
	relative_path = "../data/houses"
	full_path = path.join(absolute_path, relative_path)
	with open(full_path, 'wb') as file:
		# No need save House.n_house, count it later
		dump(House.houses_table, file)
	
	internalLog("Writing tickets data")
	relative_path = "../data/tickets"
	full_path = path.join(absolute_path, relative_path)
	with open(full_path, 'wb') as file:
		dump([House.total_tickets, House.tickets_table], file)
	
	internalLog("Data saving process finished")


def loadData(*, print_log: bool = False) -> None:
	"""
	Load `House.houses_table` from `data/houses`,
	and load `House.total_tickets` and `House.tickets_table` from `data/tickets`

	:param print_log: Whether to print logs, it is for admin mode. Keyword-only parameter
	:type print_log: bool
	:return: None
	"""
	
	logger: Logger = getLogger('loadData')
	logger.info("Loading Data")
	
	def internalLog(message: str) -> None:
		"""
		Print log if `print_log` is `True`

		:param message: Message to print
		:type message: str
		:return: None
		"""
		if print_log:
			print(message)
		logger.info(message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = "../data/houses"
	full_path = path.join(absolute_path, relative_path)
	try:
		internalLog("Finding houses data")
		with open(full_path, 'rb') as file:
			data: dict = load(file)
		House.houses_table = data
		House.n_House = len(House.houses_table)
		internalLog("Houses data loaded")
	except FileNotFoundError:
		internalLog("No houses data found")
	
	relative_path = "../data/tickets"
	full_path = path.join(absolute_path, relative_path)
	try:
		internalLog("Finding tickets data")
		with open(full_path, 'rb') as file:
			data: dict = load(file)
		House.total_tickets = data[0]
		House.tickets_table = data[1]
		internalLog("Tickets data loaded")
	except FileNotFoundError:
		internalLog("No tickets data found")
	
	internalLog("Data loading process finished")


def initLog() -> None:
	"""
	Initialize the log file
	
	:return: None
	"""
	PROGRAM_START_TIME: datetime = datetime.now()
	PROGRAM_START_TIME_STRING: str = PROGRAM_START_TIME.isoformat(sep=' ', timespec='seconds')
	PROGRAM_START_TIME_STRING: str = PROGRAM_START_TIME_STRING.replace(':', '-')  # file name can't have ':'
	absolute_path = path.dirname(__file__)
	relative_path = rf'..\logs\{PROGRAM_START_TIME_STRING}.txt'
	full_path = path.join(absolute_path, relative_path)
	head_msg: str = f"--- LOG FILE ---\nTime: {PROGRAM_START_TIME_STRING}\n"
	with open(full_path, 'w') as file:
		file.write(head_msg)
	basicConfig(
		filename=full_path,
		encoding='utf-8',
		level=DEBUG,
		format='%(asctime)s --> %(levelname)s @%(name)s --> %(message)s',
		datefmt='%Y/%m/%d %H:%M:%S',
	)
	logger: Logger = getLogger('initLog')
	logger.info('Program started')
