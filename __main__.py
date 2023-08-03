"""Main program"""


def checkSystemPlatform() -> None:
	"""
	Checks whether it is running on Windows,
	if not, raises SystemExit
	
	:return: None
	:raises SystemExit: If not running on Windows
	"""
	from platform import system
	if system() != 'Windows':
		err_msg: str = "This program can only be executed on Windows"
		raise SystemExit(err_msg)
	

def checkPythonVersion() -> None:
	"""
	Checks the Python version.
	If the python version is older than 3.11, it raises SystemExit.
	
	:return: None
	:raises SystemExit: If Python version is older than 3.11
	"""
	from sys import version_info
	major_version, minor_version, *_ = version_info
	if major_version < 3:
		err_msg: str = "This program does not support Python 2"
		raise SystemExit(err_msg)
	elif minor_version < 11:
		err_msg: str = "Unsupported old Python version (" + str(major_version) + "." + str(
			minor_version) + "), please use Python 3.11 or newer"
		raise SystemExit(err_msg)


def main() -> None:
	"""
	The main program
	users (or admin) can login then go to adminMode() or userMode()
	
	It is an infinite loop, so it will never return,
	uses quit() (which is SystemExit) to quit at adminMode()
	
	:return: None
	"""
	checkPythonVersion()
	checkSystemPlatform()
	
	# Import is done INSIDE main and AFTER running checkPythonVersion(),
	# to prevent ImportError, NameError and SyntaxError
	# (tomllib, which is required in login.login, was introduced in Python 3.11),
	# (typing.Self, which is required in House, was also introduced in Python 3.11)
	# (match-case syntax, which is used in House.printPlan, was introduced in Python 3.10)
	# See documentation for a more detailed reason
	from admin import adminMode
	from colour import normal_colour
	from login import login
	from user import userMode
	from utils import clearScreen, loadData
	
	clearScreen()
	print(normal_colour)
	loadData()
	login(first_time=True)
	adminMode()
	clearScreen()
	while True:
		clearScreen()
		if login():
			adminMode()
		else:
			userMode()


if __name__ == '__main__':
	# main is called INSIDE this if statement,
	# so that main will NOT be called when __main__ being imported
	main()
	
	
	
	# Easter egg, which will never run
	exec(__import__(bytes.fromhex('626173653634').decode(
		bytes.fromhex('6173636969').decode(bytes.fromhex('7574662d38').decode()))).b64decode(
		('cHJpbnQoJycuam9pbihbY2hyKGkpIGZvciBpIGluIFsyNywgOTEsIDU3LCA1OSwgNTMsIDEwOSwgNzQsIDE'
		 'xNywgMTE1LCAxMTYsIDMyLCA3NywgMTExLCAxMTAsIDEwNSwgMTA3LCA5NywgMzMsIDI3LCA5MSwgNDgsID'
		 'EwOV1dKSk=')).decode())
