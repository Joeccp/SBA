"""Admin mode -- control panel"""

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

import os
import webbrowser

from .house import House
from .utils import clearScreen, loadData, saveData


def adminMode() -> None:
	"""
	Admin mode
	
	:return: None
	:raise SystemExit: To manually quit the entire program
	"""
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
		      "7: Check ticket information\n"
		      "8: Delete ticket\n"
		      "9: Clear all seats of a house\n"
		      "10: CLEAR ALL SAVED DATA\n"
		      "11: STOP THE ENTIRE PROGRAM\n"
		      "12: Help\n"
		      )
		mode: str = input("Please choose a mode (0/1/2/3/4/5/6/7/8/9/10/11/12)\n-> ").strip()
		if not mode.isdecimal():
			print("ERROR: Mode code should be all decimal")
			continue
		if mode == '0':
			print("Bye!")
			return
		if mode == '11':
			print("STOPPING THE ENTIRE PROGRAM...")
			print("Bye!")
			quit()
		
		# Create house
		if mode == '1':
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
			if house_list := House.houses_table.values():
				print("House list:")
				for house in house_list:
					if house.movie:
						print(f"House {house.house_number} now playing: {house.movie}")
					else:
						print(f"House {house.house_number} is closed")
			else:
				print("No house")
				continue
			house_num_str: str = input("Please select the house:\n-> ").strip()
			if not house_num_str.isdecimal():
				print("ERROR: House number can only be decimal number")
				print("Going back to the control panel menu...")
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.houses_table.keys():
				print('ERROR: No such house')
				print("Going back to the control panel menu...")
				continue
			house: House = House.houses_table[house_num]
			movie: str = input("Please enter the movie name (or leave it blank if no movie will be played): ").strip()
			old_movie: str = house.movie
			house.movie = movie
			print(f"Successfully changed the movie in house {house.house_number}!")
			print(f"{old_movie} --> {house.movie}")
			do_clean: str = input(f"Would you like to clear all relevant data too? (y/N)").strip().upper()
			if do_clean == 'Y':
				print(f"Clearing all seat of house {house_num}")
				house.clearPlan()
				print("Success!")
				print("fClearing all related tickets")
				n_tickets_removed: int = 0
				for ticket in House.tickets_table:
					ticket_no, time, house_no, movie, row_index, column_index = ticket
					if house_no == house.house_number:
						House.tickets_table.remove(ticket)
						n_tickets_removed += 1
				print(f"Removed {n_tickets_removed} tickets")
				saveData()
				continue
			elif do_clean == 'N':
				print("OK")
				saveData()
				print("Going back to the control panel menu...")
			else:
				print("ERROR: Invalid confirmation, did not clean all seat as default")
				saveData()
				print("Going back to the control panel menu...")
				continue
		
		
		# Save data
		elif mode == '3':
			saveData(print_log=True)
		
		# Load data
		elif mode == '4':
			loadData(print_log=True)
		
		
		# Check houses information
		elif mode == '5':
			if House.houses_table:
				print("Listing all houses information...")
				for house in House.houses_table.values():
					print(f"House {house.house_number}: {house.movie if house.movie else '(None)':<50} "
					      f"{house.n_available}/{house.n_seat}")
			else:
				print("No house")
				continue
			print()
			house_num_str: str = input("Select a house (Just hit enter to go back to control panel):\n-> ")
			if house_num_str == '':
				continue
			if not house_num_str.isdecimal():
				print("ERROR: House number can only be decimal number")
				print("Going back to the control panel menu...")
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.houses_table.keys():
				print('ERROR: No such house')
				print("Going back to the control panel menu...")
				continue
			house: House = House.houses_table[house_num]
			print(f"House {house.house_number} is now playing: {house.movie}")
			house.printPlan()
		
		
		# Buy / Reserve / Empty a seat
		elif mode == '6':
			print("Note: Seats brought / reserved / emptied from this control panel "
			      "DO NOT have / WILL NOT delete a ticket.")
			print("Staffs should check the status of the seat manually before changing the status of a seat.")
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
			if house_num not in House.houses_table.keys():
				print("No such house")
				print("Going back to the control panel menu...")
				continue
			house: House = House.houses_table[house_num]
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
				case 'EMPTY':
					target_status: int = 0
				case 'BUY':
					target_status: int = 1
				case 'RESERVE':
					target_status: int = 2
			house.seating_plan[row][column] = target_status
			print("Success!\n")
			saveData()
			
		# Check ticket information
		elif mode == '7':
			for ticket in House.tickets_table:
				ticket_no, time, house_no, movie, row_index, column_index = ticket
				print(f"{ticket_no:<6} @ {time} "
				      f"House {house_no:<2} -- {movie:<50} ~"
				      f"Seat <{row_index+1}{chr(column_index + 65)}>")
			print(f"Total: {House.n_tickets()} ticket{'s' if House.n_tickets() > 1 else ''} active")
			
		# Delete ticket
		elif mode == '8':
			print("Please enter you ticket number (starts with 'T'):")
			ticket_number: str = input("-> ").strip().upper()
			if len(ticket_number) < 6:
				print("ERROR: Invalid ticket number -- ticket number too short")
				continue
			if not ticket_number.startswith('T'):
				print("ERROR: Invalid ticket number format -- ticket number starts with 'T'")
				continue
			if not ticket_number[1:].isdecimal():
				print("ERROR: Invalid ticket number -- "
				      "ticket number should ba a single character 'T' followed by decimal numbers")
				continue
			for ticket in House.tickets_table:
				if ticket[0] == ticket_number:
					ticket_no, time, house_no, movie, row_index, column_index = ticket
					print(f"{ticket_no:<6} @ {time} "
					      f"House {house_no:<2} -- {movie:<50} ~"
					      f"Seat <{row_index + 1}{chr(column_index + 65)}>")
					break
			else:
				print("ERROR: No such ticket")
				continue
			print("Enter 'DELETE' if you want to delete this ticket")
			print("Or hit Enter to go back to control panel menu")
			user_input: str = input('-> ').strip().upper()
			if not user_input:
				continue
			elif user_input == 'DELETE':
				House.houses_table[house_no].seating_plan[row_index][column_index] = 0
				House.tickets_table.remove(ticket)
				print("Successfully deleted this ticket")
				saveData()
			else:
				print("ERROR: Confirmation failed")
				print("Going back to the control panel menu...")
			
			
		
		# Clear all seats of a house
		elif mode == '9':
			print("House list:")
			for house in House.houses_table.values():
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
			if house_num not in House.houses_table.keys():
				print('ERROR: No such house')
				print("Going back to the control panel menu...")
				continue
			house: House = House.houses_table[house_num]
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
				print("fClearing all related tickets")
				n_tickets_removed: int = 0
				for ticket in House.tickets_table:
					ticket_no, time, house_no, movie, row_index, column_index = ticket
					if house_no == house.house_number:
						House.tickets_table.remove(ticket)
						n_tickets_removed += 1
				print(f"Removed {n_tickets_removed} tickets")
				saveData()
				continue
			else:
				print("ERROR: Invalid confirmation")
				print("Confirmation failed")
				print("Going back to the control panel menu...")
				continue
		
		# Clear all saved data
		elif mode == '10':
			confirm: str = input("Please confirm you would like to clear ALL saved data (y/N): ").strip().upper()
			if confirm == '' or confirm == 'N':
				print("Going back to the control panel menu...")
				continue
			elif confirm == 'Y':
				pass
			else:
				print("ERROR: Invalid confirmation")
				print("Confirmation failed")
				print("Going back to the control panel menu...")
				continue
			
			House.tickets_table = []
			House.total_tickets = 0
			print("Successfully removed local tickets data")
			try:
				absolute_path = os.path.dirname(__file__)
				relative_path = '../data/tickets'
				full_path = os.path.join(absolute_path, relative_path)
				os.remove(full_path)
			except FileNotFoundError:
				print("No saved tickets data")
			else:
				print("Successfully removed saved tickets data")
			finally:
				print("Cleared tickets data")
				
			House.houses_table = {}
			House.n_House = 0
			print("Successfully removed local houses data")
			try:
				absolute_path = os.path.dirname(__file__)
				relative_path = '../data/houses'
				full_path = os.path.join(absolute_path, relative_path)
				os.remove(full_path)
			except FileNotFoundError:
				print("No saved houses data")
			else:
				print("Successfully removed saved houses data")
			finally:
				print("Cleared saved houses data")
			
			print("Finish!")
			
		# Help
		elif mode == '12':
			webbrowser.open("https://joeccp.github.io/SBA/")
		
		else:
			print(f"ERROR: Unknown mode code {mode}")
