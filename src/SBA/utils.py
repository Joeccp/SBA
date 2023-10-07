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


from atexit import register
from datetime import datetime
from logging import basicConfig, DEBUG, getLogger, Logger
from os import get_terminal_size, name, makedirs, path, system
from pickle import dump, load
from platform import system as systemPlatform  # NOQA: lowercase function imported as uppercase function
from sys import argv, version_info

from .colour import loadColour, setColour
from .house import House
from .language import loadLanguage, printLang, setLanguage


class RealExit(Exception):
	"""
	This exception is raised when you really want to quit
	i.e. Not an unexpected program crash
	
	This exception should be handled specially in main.main()
	
	Do NOT use exit() or quit() or even os._exit(), they can't be treated specifically (in this program)
	"""
	
	def __init__(self, message: str = "") -> None:
		# No logging is needed
		self.message: str = message
		super().__init__(self.message)


def checkPythonVersion() -> None:
	"""
	Checks the Python version.
	If the python version is older than 3.11, it raises SystemExit.

	:return: None
	:raises SystemExit: If the Python version is older than 3.11
	"""
	# (tomllib, which is required in login.login, was introduced in Python 3.11),
	# (typing.Self, which is used in house.House, was also introduced in Python 3.11)
	# (match-case syntax, which is used in House.printPlan, was introduced in Python 3.10)
	
	logger: Logger = getLogger("checkPythonVersion")
	major_version, minor_version, *_ = version_info
	if major_version < 3:
		logger.critical("I am running on Python %s!", major_version)
		logger.critical("QUITTING THE PROGRAM: Python version lower than Python 3.11")
		err_msg: str = "This program does not support Python 2"
		raise RealExit(err_msg)
	elif minor_version < 11:
		logger.critical("I am running on Python 3.%s!", minor_version)
		logger.critical("QUITTING THE PROGRAM: Python version lower than Python 3.11")
		err_msg: str = "Unsupported old Python version (" + str(major_version) + "." + str(
			minor_version) + "), please use Python 3.11 or newer"
		raise RealExit(err_msg)


def clearScreen() -> None:
	"""
	Clear the screen

	:return: None
	"""
	
	try:
		terminal_width, terminal_height = get_terminal_size()
		# Print empty lines in case system('cls') or system('clear') does not work
		print('\n' * terminal_height, end='')
	except OSError:
		# OSError: [WinError 6] The handle is invalid
		# Normally due to get_terminal_size()
		# But still need to print empty lines in case system('cls') or system('clear') does not work
		print('\n' * 30)
	finally:
		if name == 'nt':
			system('cls')
		else:
			system('clear')


def saveData(*, print_log: bool = False) -> None:
	"""
	Save `House.houses_table` into `data/houses`,
	and save `House.total_tickets` and `House.tickets_table` into `data/tickets`
	
	:param print_log: Whether to print logs, it is for admin mode. Keyword-only parameter
	:type print_log: bool
	:return: None
	"""
	from .colour import colour_mode
	from .language import language
	
	logger: Logger = getLogger('saveData')
	logger.info("Saving Data")
	
	def internalLog(english_message: str, chinese_message: str) -> None:
		"""
		Print (English) log if `print_log` is `True`

		:param english_message: An English message to print and log
		:type english_message: str
		:param chinese_message: A Chinese message to print
		:type chinese_message: str
		:return: None
		"""
		if print_log:
			printLang(english_message, chinese_message)
		logger.info(english_message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = '../../data'
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	internalLog("Reaching the data folder", "正在尋找 data 資料夾")
	if not path.isdir(full_path):
		internalLog("No data folder, creating one", "無 data 資料夾，正在創建")
		makedirs(full_path)
	
	internalLog("Writing houses data", "正在寫入電影院資料")
	relative_path = "../../data/houses"
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	with open(full_path, 'wb') as file:
		# No need save House.n_house, count it later
		dump(House.houses_table, file)
	
	internalLog("Writing tickets data", "正在寫入電影票資料")
	relative_path = "../../data/tickets"
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	with open(full_path, 'wb') as file:
		dump([House.total_tickets, House.tickets_table], file)
	
	internalLog("Writing colour scheme setting", "正在寫入顔色設定")
	setColour(colour_mode)
	
	internalLog("Writing language option", "正在寫入語言設定")
	setLanguage(language)
	
	internalLog("Data saving process finished", "儲存資料程序完成")


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
	
	def internalLog(english_message: str, chinese_message: str) -> None:
		"""
		Print (English) log if `print_log` is `True`

		:param english_message: An English message to print and log
		:type english_message: str
		:param chinese_message: A Chinese message to print
		:type chinese_message: str
		:return: None
		"""
		if print_log:
			printLang(english_message, chinese_message)
		logger.info(english_message)
	
	absolute_path = path.dirname(__file__)
	
	relative_path = "../../data/houses"
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	try:
		internalLog("Finding houses data", "正在尋找電影院資料")
		with open(full_path, 'rb') as file:
			data: dict = load(file)
		House.houses_table = data
		House.n_House = len(House.houses_table)
		internalLog("Houses data loaded", "已載入電影院資料")
	except FileNotFoundError:
		internalLog("No houses data found", "無電影院資料")
	
	relative_path = "../../data/tickets"
	full_path = path.join(absolute_path, relative_path)
	logger.debug(f"Full path = {full_path}")
	try:
		internalLog("Finding tickets data", "正在尋找電影票資料")
		with open(full_path, 'rb') as file:
			data: dict = load(file)
		House.total_tickets = data[0]
		House.tickets_table = data[1]
		internalLog("Tickets data loaded", "已載入電影票資料")
	except FileNotFoundError:
		internalLog("No tickets data found", "無電影票資料")
	
	internalLog("Loading colour scheme", "正在載入配色設定")
	loadColour()
	internalLog("Colour scheme loaded", "已載入配色設定")
	
	internalLog("Loading language setting", "正在載入語言設定")
	loadLanguage()
	internalLog("Colour scheme loaded", "已載入語言設定")
	
	internalLog("Data loading process finished", "載入資料程序完成")


LOG_FILE_FULL_PATH: str = ''


def initLog() -> None:
	"""
	Initialize the log file
	
	:return: None
	"""
	global LOG_FILE_FULL_PATH
	PROGRAM_START_TIME: datetime = datetime.now()
	PROGRAM_START_TIME_STRING: str = PROGRAM_START_TIME.isoformat(sep=' ', timespec='seconds')
	PROGRAM_START_TIME_STRING: str = PROGRAM_START_TIME_STRING.replace(':', '-')  # file name can't have ':'
	absolute_path = path.dirname(__file__)
	relative_path = f'../../logs/{PROGRAM_START_TIME_STRING}.txt'
	full_path = path.join(absolute_path, relative_path)
	LOG_FILE_FULL_PATH = full_path
	head_msg: str = (f"--- LOG FILE ---\n"
	                 "~INFO~\n"
	                 f"    Time: {PROGRAM_START_TIME_STRING}\n"
	                 f"    Python version: {version_info.major}.{version_info.minor}.{version_info.micro}\n"
	                 f"    Arguments: {argv}\n"
	                 f"    Path: {path.abspath(__file__)}\n"
	                 f"~INFO~\n")
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


@register
def endLog() -> None:
	"""
	Log message when exiting
	
	:return: None
	"""
	try:
		with open(LOG_FILE_FULL_PATH, 'a') as file:
			file.write('--- LOG FILE ---')
	except FileNotFoundError:
		pass
