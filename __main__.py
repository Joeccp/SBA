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
	while True:
		print("To initialize, please login as admin.")
		result: int = login()
		if result == 0:
			print("Sorry, only admin can log in as initialization is required.")
			continue
		else:
			break
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
