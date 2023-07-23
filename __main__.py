"""Main program"""
from house import House
from common import clearScreen, checkPythonVersion
from login import login
from colour import normal
from admin import adminMode
from user import userMode


def main() -> None:
	checkPythonVersion()
	clearScreen()
	print(normal)
	print("CINEMA KIOSK SYSTEM\n\n\n")
	print("To initialize, please login as admin.")
	login(_first_time=True)
	adminMode()
	clearScreen()
	while True:
		clearScreen()
		if login() == 1:
			adminMode()
		else:
			userMode()
	


if __name__ == '__main__':
	main()
	print("\033[9;5mJust Monika!\033[0m")
