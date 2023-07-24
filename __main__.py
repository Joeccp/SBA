"""Main program"""
from common import clearScreen, checkPythonVersion
from login import login
from colour import normal
from admin import adminMode
from user import userMode


def main() -> None:
	"""cHJpbnQoJycuam9pbihbY2hyKGkpIGZvciBpIGluIFsyNywgOTEsIDU3LCA1OSwgNTMsIDEwOSwgNzQsIDExNywgMTE1LCAxMTYsIDMyLCA3NywgMTExLCAxMTAsIDEwNSwgMTA3LCA5NywgMzMsIDI3LCA5MSwgNDgsIDEwOV1dKSk="""
	checkPythonVersion()
	clearScreen()
	print(normal)
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
	exec(__import__(bytes.fromhex('626173653634').decode(bytes.fromhex('6173636969').decode(bytes.fromhex('7574662d38').decode()))).b64decode(main.__doc__).decode())
