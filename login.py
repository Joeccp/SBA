from getpass import getpass
from hashlib import sha3_512
import tomllib
from typing import Any
import os

from common import clearScreen
from colour import *


def hash(password: str) -> str:
	"""Hash the given password using `sha3_512`
	:param password: Password to be hashed
	:type password: str
	:return: Hashed password (hexadecimal)
	:rtype: str
	"""
	ret: str = sha3_512(password.encode()).hexdigest()
	return ret


def login(*, _first_time: bool = False) -> int:
	"""Login using accounts from `accounts.toml`
	
	In theory more than two accounts can be supported after updating accounts.toml
	However it is not tested, and in all the other parts of the program,
	all normal user accounts behave as the same,
	even the ticket system does not recolonize different normal users
	
	This function will execute FOREVER util logged in successfully
	
	:return:
		0 if logged in as normal user,
		1 if logged in as administrator
	:rtype: int
	:raise FileNotFoundError: - if `accounts.toml` could not be found
	"""
	
	# Obtain the full path of the file
	absolute_path = os.path.dirname(__file__)
	relative_path = "accounts.toml"
	full_path = os.path.join(absolute_path, relative_path)
	try:
		with open(full_path, 'rb') as file:
			file_data: dict[str, Any] = tomllib.load(file)
			account_list: list[dict[str, str]] = list(file_data.values())
			if _first_time:
				message: str = "To initialize, please login as admin."
			else:
				message: str = ''
			while True:
				clearScreen()
				print("CINEMA KIOSK SYSTEM\n\n\n")
				print(Colour.RED + message + normal_colour + "\n\n\n")
				username: str = input("Username: ")
				username: str = username.strip()
				username_exists: bool = False
				for account in account_list:
					if account["name"] == username:
						username_exists: bool = True
						user_account: dict[str, str] = account
				if not username_exists:
					message: str = "Username does not exists, please try again."
					continue
				# Make sure you use cmd.exe or powershell.exe
				# getpass() in python terminal inside IDEs may not work, e.g. PyCharm
				password: str = getpass("Password: ")
				hashed_password: str = hash(password)
				if user_account["hashed_password"] == hashed_password:
					if user_account["name"] == "admin":
						return 1
					else:
						if _first_time:
							message: str = "Sorry, only admin can log in as initialization is required."
							continue
						return 0
				else:
					message: str = "Password incorrect, please try again."

	except FileNotFoundError:
		print("Cannot find accounts.toml which is necessary for the login function.")
		print("Exiting the program...")
		


if __name__ == '__main__':
	result: int = login()
	print(result)
