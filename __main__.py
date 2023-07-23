"""Main program"""
from house import House
from common import clearScreen, checkPythonVersion
from login import login
from typing import *
from colour import Colour, normal, row_colour, column_colour
from admin import adminMode


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
	while True:
		if login() == 1:
			adminMode()
		else:
			...
	


if __name__ == '__main__':
	main()
