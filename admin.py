"""Admin mode -- control panel"""

from colour import Colour, normal, row_colour, column_colour
from House import House
from common import clearScreen


def adminMode() -> None:
	clearScreen()
	print("CINEMA KIOSK SYSTEM")
	print("CONTROL PANEL\n\n\n")
	while True:
		print("\n"
		      "0: EXIT CONTROL PANEL\n"
		      "1: Create house\n"
		      "2: Update movie\n"
		      "3: Save data\n"
		      "4: Load data\n"
		      "5: Check houses information\n"
		      "6: Buy / Reserve / Empty a seat\n"
		      "7: Clear all seats of a house"
		      "8: CLEAR SAVED DATA\n"
		      "9: STOP THE ENTIRE PROGRAM"
		      )
		mode: str = input("Please enter the action you want to perform (0/1/2/3/4/5/6/7/8/9)\n-> ").strip()
		if not mode.isdecimal():
			print("ERROR: Action code should be all decimal")
			continue
		if mode not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
			print("ERROR: Unknown Action code")
			continue
		if mode == '0':
			print("Bye!")
			return
		if mode == '9':
			print("STOPPING THE ENTIRE PROGRAM...")
			print("Bye!")
			quit()
		
		# Create house
		elif mode == '1':
			print(f"House {House.n_House + 1} will be the new house")
			n_row_str: str = input(f"Enter how many row does House {House.n_House + 1} has (1-99): ").strip()
			if not n_row_str.isdecimal():
				print("ERROR: Number of rows must be decimal number")
				print("House creation failed, exiting to control panel menu...")
				continue
			n_row: int = int(n_row_str)
			if n_row > 99:
				print("Unsupported large number of rows")
				print("House creation failed, exiting to control panel menu...")
				continue
			n_col_str: str = input(f"Enter how many column does House {House.n_House + 1} has (1-26): ").strip()
			if not n_col_str.isdecimal():
				print("ERROR: Number of columns must be decimal number")
				print("House creation failed, exiting to control panel menu...")
				continue
			n_col: int = int(n_col_str)
			if n_col > 26:
				print("Unsupported large number of columns")
				print("House creation failed, exiting to control panel menu...")
				continue
			house: House = House(row_number=n_row, column_number=n_col)
			movie: str = input("Please enter the movie name (or leave it blank if no movie will be played): ").strip()
			if movie == '':
				pass
			else:
				house.movie = movie
			print("Success!")
		
		# Update movie
		elif mode == '2':
			print("House list:")
			for house in House.table.values():
				if house.movie:
					print(f"House {house.house_number} now playing: {house.movie}")
				else:
					print(f"House {house.house_number} is closed")
			house_num_str: str = input("Please select the house:\n-> ").strip()
			if not house_num_str.isdecimal():
				print("ERROR: House number can only be decimal number")
				print("Going back to the control panel menu...")
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.table.keys():
				print('ERROR: No such house')
				print("Going back to the control panel menu...")
				continue
			house: House = House.table[house_num]
			movie: str = input("Please enter the movie name (or leave it blank if no movie will be played): ").strip()
			old_movie: str = house.movie
			house.movie = movie
			print(f"Successfully changed the movie in house {house.house_number}!")
			print(f"{old_movie} --> {house.movie}")
			do_clean: str = input(f"Would you like to clear the seating plan too? (y/N)").strip().upper()
			if do_clean == 'Y':
				print(f"Clearing all seat of house {house_num}")
				house.clearPlan()
				print("Success!")
				continue
			elif do_clean == 'N':
				print("OK")
				print("Going back to the control panel menu...")
			else:
				print("ERROR: Invalid confirmation, did not clean all seat as default")
				print("Going back to the control panel menu...")
				continue
		
		
		# Save data
		elif mode == '3':
			...
		
		# Load data
		elif mode == '4':
			...
		
		# Check houses information
		elif mode == '5':
			print("Listing all houses information...")
			for house in House.table.values():
				print(f"House {house.house_number}: {house.movie if house.movie else '(None)':<50} "
				      f"{house.available}/{house.n_seat}")
			house_num_str: str = input("Select a house (Just hit enter to go back to control panel):\n-> ")
			if not house_num_str.isdecimal():
				print("ERROR: House number can only be decimal number")
				print("Going back to the control panel menu...")
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.table.keys():
				print('ERROR: No such house')
				print("Going back to the control panel menu...")
				continue
			house: House = House.table[house_num]
			print(f"House {house.house_number} is now playing: {house.movie}")
			house.printPlan()
		
		
		# Buy / Reserve / Empty a seat
		elif mode == '6':
			print("Note: Seats brought / reserved / emptied from this control panel WILL NOT be given a ticket.")
			print("You should check the status of the seat before changing the status of a seat.")
			print("The program will NOT check the seat status for you.")
			print("""Command format:\n\n"""
			      """BUY [HOUSE NUMBER] [ROW NUMBER] [COLUMN INDEX]             --- Buy a seat\n"""
			      """RESERVED [HOUSE NUMBER] [ROW NUMBER] [COLUMN INDEX]        --- Reserve a seat\n"""
			      """EMPTY [HOUSE NUMBER] [ROW NUMBER] [COLUMN INDEX]           --- Empty a seat\n"""
			      """(or hit Enter to go back to control panel menu)"""
			      )
			command: str = input("-> ").strip().upper()
			if command == '':
				continue
			command_separated: list[str] = command.split()
			if len(command_separated) != 4:
				print("ERROR: Syntax of command line is wrong")
				print("Going back to the control panel menu...")
				continue
			action: str = command_separated[0]
			if action not in ('BUY', 'RESERVE', 'EMPTY'):
				print(f"ERROR: Unknown operation -- {command_separated[0]}")
				print("Going back to the control panel menu...")
				continue
			if not command_separated[1].isdecimal():
				print("ERROR: House number should be a decimal number")
				print("Going back to the control panel menu...")
				continue
			house_num: int = int(command_separated[1])
			if house_num not in House.table.keys():
				print("No such house")
				print("Going back to the control panel menu...")
				continue
			house: House = House.table[house_num]
			if not command_separated[2].isdecimal():
				print("Row number must be a decimal number")
				print("Going back to the control panel menu...")
				continue
			row: int = int(command_separated[2])
			if row == 0:
				print("ERROR: Row number cannot be zero, and is starting from 1")
				print("Going back to the control panel menu...")
				continue
			if row > house.n_row:
				print("ERROR: No such row")
				print("Going back to the control panel menu...")
				continue
			row: int = row - 1  # Row index starts from 0 in python
			if len(command_separated[3]) > 1:
				print("ERROR: Column index can only be A-Z, which is one single character")
				print("Going back to the control panel menu...")
				continue
			if not 65 <= ord(command_separated[3]) <= 90:  # ASCII A-Z is 65-90
				print("ERROR: Column index should be a single character from A to Z")
				print("Going back to the control panel menu...")
				continue
			column: int = ord(command_separated[3]) - 64
			if column > house.n_column:
				print("No such column")
				print("Going back to the control panel menu...")
				continue
			column: int = column - 1  # Column index starts from 0 in python
			match action:
				case 'BUY':
					target_status: int = 1
				case 'EMPTY':
					target_status: int = 0
				case 'RESERVE':
					target_status: int = 2
				case _:
					raise RuntimeError("Action code matched with nothing. This should be impossible.")
			house.plan[row][column] = target_status
			print("Success!\n")
			
			

			
		
		# Clear all seats of a house
		elif mode == '7':
			print("House list:")
			for house in House.table.values():
				if house.movie:
					print(f"House {house.house_number} now playing: {house.movie}")
				else:
					print(f"House {house.house_number} is closed")
			house_num_str: str = input("Which house would you like to empty:\n-> ")
			if not house_num_str.isdecimal():
				print("ERROR: House number can only be decimal number")
				print("Going back to the control panel menu...")
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.table.keys():
				print('ERROR: No such house')
				print("Going back to the control panel menu...")
				continue
			house: House = House.table[house_num]
			print(f"House {house_num}")
			house.printPlan()
			confirm: str = input("Please confirm you would like to clear all seat (y/N): ").strip().upper()
			if confirm == '' or confirm == 'N':
				print("Going back to the control panel menu...")
				continue
			elif confirm == 'Y':
				print(f"Clearing all seat of house {house_num}")
				house.clearPlan()
				print("Success!")
				continue
			else:
				print("ERROR: Invalid confirmation")
				print("Going back to the control panel menu...")
				continue
		
		# Clear all saved data
		elif mode == '8':
			...
		
		else:
			raise RuntimeError(f"RUNTIME-ERROR: Unknown mode action: {mode}")


if __name__ == '__main__':
	adminMode()
	print("\033[9;5mJust Monika!\033[0m")
	