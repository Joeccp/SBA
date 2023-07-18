from getpass import getpass
from hashlib import sha3_512
import tomllib
from typing import Any
import os


def hash(password: str) -> str:
	"""Hash the given password using sha3_512
	:param password: Password to be hashed
	:type password: str
	:return: Hashed password (hexadecimal)
	:rtype: str
	"""
	ret: str = sha3_512(password.encode()).hexdigest()
	return ret


def login() -> int:
	"""Login using accounts from accounts.toml
	Hard-coded to be only support the administrator and user account
	This function will execute FOREVER util logged in successfully
	:return: 0 if logged in as normal user, 1 if logged in as administrator
	:rtype: int
	"""
	
	# Obtain the relative path
	# Credit: https://towardsthecloud.com/get-relative-path-python
	# ****************************************************
	absolute_path = os.path.dirname(__file__)
	relative_path = "accounts.toml"
	full_path = os.path.join(absolute_path, relative_path)
	# ****************************************************
	
	with open(full_path, 'rb') as file:
		file_data: dict[str, Any] = tomllib.load(file)
		account_list: list[dict[str, str]] = list(file_data.values())
		while True:
			username: str = input("Username: ")
			username: str = username.strip()
			username_exists: bool = False
			for account in account_list:
				if account["name"] == username:
					username_exists: bool = True
					user_account: dict[str, str] = account
			if not username_exists:
				print("Username does not exists, please try again.")
				continue
			# Make sure you use cmd.exe or powershell.exe
			# getpass() in python terminal inside IDE may not work
			password: str = getpass("\rPassword: ")
			hashed_password: str = hash(password)
			if user_account["hashed_password"] == hashed_password:
				if user_account["name"] == "admin":
					return 1
				else:
					return 0
			else:
				print("Password incorrect, please try again.")
				continue


if __name__ == '__main__':
	result: int = login()
	print(result)
