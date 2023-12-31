"""Login function"""

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


from getpass import getpass
from hashlib import sha3_512
from logging import getLogger, Logger
from os import path
from tomllib import load as loadtoml
from typing import Any

from .colour import Colour
from .language import inputLang, printLang
from .utils import clearScreen


def hash(password: str) -> str:
	"""
	Hash the given password using `sha3_512`
	:param password: Password to be hashed
	:type password: str
	:return: Hashed password (hexadecimal)
	:rtype: str
	"""
	ret: str = sha3_512(password.encode()).hexdigest()
	return ret


def login(*, first_time: bool = False) -> int:
	"""
	Login using accounts from `data/accounts.toml`
	
	In theory more than two accounts can be supported after updating accounts.toml
	However it is not officially supported, and in all the other parts of the program,
	all normal user accounts behave like the same,
	even the ticket system does not recolonize different normal users
	
	This function will execute FOREVER util logged in successfully
	
	:param first_time: Keyword-only parameter,
		to identify whether it is the first time logging in and requires login as administrator
	:type first_time: bool
	:return:
		0 if logged in as normal user,
		1 if logged in as administrator
	:rtype: int
	:raise FileNotFoundError: If `accounts.toml` could not be found
	"""
	from .colour import normal_colour
	from .language import language
	
	logger: Logger = getLogger('login')
	
	logger.info("Reaching accounts.toml file")
	# Obtain the full path of the file
	absolute_path = path.dirname(__file__)
	relative_path = "../../data/accounts.toml"
	full_path = path.join(absolute_path, relative_path)
	try:
		with open(full_path, 'rb') as file:
			logger.info("Getting accounts information")
			file_data: dict[str, Any] = loadtoml(file)
			account_list: list[dict[str, str]] = list(file_data.values())
			if first_time:
				if language == 'ENGLISH':
					message: str = "To initialize, please login as admin."
				else:
					message: str = "請登錄為管理員以初始化系統。"
				logger.info("First time logging in, requires login as admin")
			else:
				message: str = ''
			while True:
				clearScreen()
				printLang("CINEMA KIOSK SYSTEM\n\n\n", "電影售票系統\n\n\n")
				print(Colour.RED + message + normal_colour + "\n\n\n")
				logger.info("Waiting username input")
				username: str = inputLang("Username: ", "用戶名稱：")
				username: str = username.strip()
				if username == '':
					message: str = ''
					continue
				username_exists: bool = False
				for account in account_list:
					if account["name"] == username:
						username_exists: bool = True
						user_account: dict[str, str] = account
				if not username_exists:
					logger.info("Username doesn't exit")
					if language == 'ENGLISH':
						message: str = "Username does not exists, please try again."
					else:
						message: str = "用戶名稱不存在，請重新輸入。"
					continue
				# Make sure you use cmd.exe or powershell.exe
				# getpass() in python terminal inside IDEs may not work, e.g. PyCharm
				if language == 'ENGLISH':
					prompt: str = "Password: "
				else:
					prompt: str = "密碼："
				password: str = getpass(prompt).strip()
				hashed_password: str = hash(password)
				if user_account["hashed_password"] == hashed_password:
					if user_account["name"] == "admin":
						logger.info("LOGGED IN AS ADMIN")
						return 1
					else:  # Login as user success
						if first_time:
							logger.info("USER WANTS TO LOGIN BUT ONLY ADMIN CAN LOGIN NOW")
							if language == 'ENGLISH':
								message: str = "Sorry, only admin can log in now as initialization is required."
							else:
								message: str = "抱歉，現在只有管理員才能登錄。"
							continue
						logger.info("LOGGED IN AS USER")
						return 0
				else:
					logger.info("Incorrect password")
					if language == 'ENGLISH':
						message: str = "Password incorrect, please try again."
					else:
						message: str = "密碼錯誤，請重新登錄。"
	
	except FileNotFoundError:
		logger.critical("No accounts.toml file")
		logger.critical("QUITTING THE PROGRAM: No accounts information")
		# Important error message for a critical error, no translation is needed (to prevent further error)
		print("Cannot find accounts.toml which is necessary for the login function.")
		print("Exiting the program...")
		quit()
