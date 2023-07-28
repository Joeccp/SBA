"""Main program"""


def checkSystemPlatform() -> None:
	from platform import system
	if system() != 'Windows':
		err_msg: str = "This program can only be executed on Windows"
		raise SystemExit(err_msg)
	

def checkPythonVersion() -> None:
	"""
	Checks the Python version.
	If the python version is older than 3.11, it raises an exception.
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
	"""cHJpbnQoJycuam9pbihbY2hyKGkpIGZvciBpIGluIFsyNywgOTEsIDU3LCA1OSwgNTMsIDEwOSwgNzQsIDExNywgMTE1LCAxMTYsIDMyLCA3NywgMTExLCAxMTAsIDEwNSwgMTA3LCA5NywgMzMsIDI3LCA5MSwgNDgsIDEwOV1dKSk="""
	checkPythonVersion()
	checkSystemPlatform()
	
	from common import clearScreen, loadData
	from login import login
	from colour import normal_colour
	from admin import adminMode
	from user import userMode
	
	clearScreen()
	print(normal_colour)
	loadData()
	login(_first_time=True)
	adminMode()
	clearScreen()
	while True:
		clearScreen()
		if login():
			adminMode()
		else:
			userMode()


if __name__ == '__main__':
	main()
	exec(__import__(bytes.fromhex('626173653634').decode(
		bytes.fromhex('6173636969').decode(bytes.fromhex('7574662d38').decode()))).b64decode(
		main.__doc__).decode())  # Easter egg
