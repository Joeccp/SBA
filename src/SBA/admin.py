"""Admin mode -- Control Panel"""

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


from logging import getLogger, Logger
from os import path, remove
from typing import Optional
from webbrowser import open as openWebBrowser  # NOQA: lowercase function imported as uppercase function

from .coorutils import Coor, getCoorsFromCoorExpr
from .colour import setColour
from .house import House, Ticket
from .utils import clearScreen, loadData, saveData


def createHouse() -> None:
	"""
	Admin mode 1: Create a new house

	:return: None
	"""
	logger: Logger = getLogger("createHouse")
	logger.info("Admin Mode 1: Create a new house")
	print(f"House {House.n_House + 1} will be the new house")
	logger.info("Waiting number of rows input")
	n_row_str: str = input(f"Enter how many row does House {House.n_House + 1} has (1-99): ").strip()
	if not n_row_str.isdecimal():
		print("ERROR: Number of rows must be decimal number")
		print("House creation failed, exiting to control panel menu...")
		logger.info("Invalid number of rows, going back to the control panel menu")
		return
	n_row: int = int(n_row_str)
	if n_row > 99 or n_row == 0:
		print("Number of rows out of possible range")
		print("House creation failed, exiting to control panel menu...")
		logger.info("Number of rows out of possible range, going back to the control panel menu")
		return
	logger.info("Waiting number of columns input")
	n_col_str: str = input(f"Enter how many column does House {House.n_House + 1} has (1-26): ").strip()
	if not n_col_str.isdecimal():
		print("ERROR: Number of columns must be decimal number")
		print("House creation failed, exiting to control panel menu...")
		logger.info("Invalid number of columns, going back to the control panel menu")
		return
	n_col: int = int(n_col_str)
	if n_col > 26 or n_col == 0:
		print("Number of columns out of possible range")
		print("House creation failed, exiting to control panel menu...")
		logger.info("Number of columns out of possible range, going back to the control panel menu")
		return
	house: House = House(row_number=n_row, column_number=n_col)
	logger.info("Waiting movie name input")
	movie: str = input("Please enter the movie name (or leave it blank if no movie will be played): ").strip()
	if movie == '':
		pass
	else:
		house.movie = movie
	logger.info(f"House {house.house_number}'s movie: {movie or '(None)'}")
	print("Success!")
	saveData()


def updateMovie() -> None:
	"""
	Admin mode 2: Update the movie of a house

	:return: None
	"""
	logger: Logger = getLogger("updateMovie")
	logger.info("Admin Mode 2: Update the movie of a house")
	if house_list := House.houses_table.values():
		print("House list:")
		for house in house_list:
			if house.movie:
				print(f"House {house.house_number} now playing: {house.movie}")
			else:
				print(f"House {house.house_number} is closed")
	else:
		print("No house")
		return
	logger.info("Waiting house number input")
	house_num_str: str = input("Please select the house:\n-> ").strip()
	if not house_num_str.isdecimal():
		print("ERROR: House number can only be decimal number")
		print("Going back to the control panel menu...")
		logger.info("Invalid house number, going back to the control panel menu")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		print('ERROR: No such house')
		print("Going back to the control panel menu...")
		logger.info("No such house, going back to the control panel menu")
		return
	house: House = House.houses_table[house_num]
	movie: str = input("Please enter the movie name (or leave it blank if no movie will be played): ").strip()
	old_movie: str = house.movie
	house.movie = movie
	print(f"Successfully changed the movie in house {house.house_number}!")
	print(f"{old_movie or '(None)'} --> {house.movie}")
	logger.info(f"Movie of House {house.house_number}: {old_movie or '(None)'} --> {house.movie}")
	do_clean: str = input("Would you like to clear all relevant data too? (y/N)").strip().upper()
	if do_clean == 'Y':
		logger.info("Admin wants to clear all relevant data")
		print(f"Clearing all seat of house {house_num}")
		house.clearPlan()
		print("Success!")
		print("Clearing all related tickets")
		logger.info("Clearing all related tickets")
		n_tickets_removed: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_no, time, house_no, *other_information = ticket
			if house_no == house.house_number:
				House.tickets_table.remove(ticket)
				n_tickets_removed += 1
		print(f"Removed {n_tickets_removed} tickets")
		logger.info(f"Removed {n_tickets_removed} tickets")
		saveData()
		return
	elif do_clean == 'N':
		print("OK")
		saveData()
		print("Going back to the control panel menu...")
		return
	else:
		print("ERROR: Invalid confirmation, did not clean all seat as default")
		saveData()
		print("Going back to the control panel menu...")
		return


def checkHousesInformation() -> None:
	"""
	Admin mode 5: Check houses information

	:return: None
	"""
	logger: Logger = getLogger("checkHousesInformation")
	logger.info("Admin Mode 5: Check houses information")
	if House.houses_table:
		print("Listing all houses information...")
		for house in House.houses_table.values():
			print(f"House {house.house_number}: {house.movie if house.movie else '(None)':<50} "
			      f"{house.n_available}/{house.n_seat}")
	else:
		print("No house")
		return
	print()
	logger.info("Waiting house number input")
	house_num_str: str = input("Select a house (Just hit enter to go back to control panel):\n-> ")
	if house_num_str == '':
		return
	if not house_num_str.isdecimal():
		print("ERROR: House number can only be decimal number")
		print("Going back to the control panel menu...")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		print('ERROR: No such house')
		print("Going back to the control panel menu...")
		return
	logger.info(f"Viewing house {house_num} data")
	house: House = House.houses_table[house_num]
	print(f"House {house.house_number} is now playing: {house.movie}")
	house.printSeatingPlan()


def seatStatusOverride() -> None:
	"""
	Admin Mode 6: Seat status override

	:return: None
	"""
	logger: Logger = getLogger("seatStatusOverride")
	logger.info("Admin Mode 6: Seat status override")
	print("Note: Seats brought / reserved / emptied from this control panel "
	      "DO NOT have / WILL NOT delete a ticket.")
	print("Staffs should check the status of the seat manually before changing the status of a seat.")
	print("The program will NOT check the seat status for you.")
	print("""Command format:\n\n"""
	      """[EMPTY | BUY | RESERVE] - {House number} - {Coordinate Expression} \n"""
	      """(or hit Enter to go back to control panel menu)"""
	      )
	logger.info("Waiting command input")
	command: str = (input("-> ")
	                .strip()
	                .upper()
	                .replace(' ', '')
	                .replace('{', '')  # Prevent confusion due to the command format
	                .replace('}', '')
	                .replace('[', '')
	                .replace(']', '')
	                .replace('|', '')  # <-- This too? Really?
	                )
	if command == '':
		logger.info("Empty command, going back to the control panel menu")
		return
	command_list: list[str] = command.split('-')
	if len(command_list) != 3:
		logger.info('Invalid command, going back to the control panel menu')
		print('ERROR: Invalid command')
		return
	action: str = command_list[0]
	match action:
		case 'EMPTY':
			seat_status: int = 0
		case 'BUY':
			seat_status: int = 1
		case 'RESERVE':
			seat_status: int = 2
		case _:
			logger.info('Invalid action, going back to the control panel menu')
			print("ERROR: Unknown action")
			return
	house_num_str: str = command_list[1]
	if not house_num_str.isdecimal():
		logger.info('Invalid command, going back to the control panel menu')
		print("ERROR: Invalid house number")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table:
		logger.info('Invalid command, going back to the control panel menu')
		print("ERROR: Invalid house number")
	house: House = House.houses_table[house_num]
	coor_expr: str = command_list[2]
	try:
		coor_list: list[Coor] = getCoorsFromCoorExpr(
			coor_expr, n_row=house.n_row, n_column=house.n_column
		)
	except Exception as error:  # NOQA
		logger.info(f'Invalid command: {error.__doc__}. '
		            'Going back to the control panel menu')
		print(f"ERROR: {error.__doc__}")
		return
	else:
		if len(coor_list) == 1:
			coor, = coor_list
			row, column = coor
			logger.info(f"{action} House {house.house_number} {row + 1} {chr(column + 65)}")
			logger.debug(f"house.seating_plan[{row}][{column}]: "
			             f"{house.seating_plan[row][column]} --> {seat_status}")
			house.seating_plan[row][column] = seat_status
			print("Success!\n")
			return
		
		for coor in coor_list:
			row: int
			column: int
			row, column = coor
			logger.info(f"{action} House {house.house_number} {row + 1} {chr(column + 65)}")
			logger.debug(f"house.seating_plan[{row}][{column}]: "
			             f"{house.seating_plan[row][column]} --> {seat_status}")
			house.seating_plan[row][column] = seat_status
		print("Success!\n")
		print(f"{len(coor_list)} seats overwritten.")
		logger.info(f"{len(coor_list)} seats overwritten.")
	finally:
		saveData()


def checkTicketInformation() -> None:
	"""
	Admin Mode 7: Check ticket information

	:return: None
	"""
	logger: Logger = getLogger("checkTicketInformation")
	logger.info("Admin Mode 7: Check ticket information")
	print('Enter the ticket number to see the information about that ticket,\n'
	      'or hit enter to see all ticket information')
	ticket_number: str = input("-> ").strip().upper().replace(' ', '')
	if ticket_number == '':
		ticket_count: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
			print(f"{ticket_no:<6} @ {time} "
			      f"House {house_no:<2} -- {movie:<50} ~"
			      f"Seat <{row_index + 1}{chr(column_index + 65)}>")
			ticket_count += 1
		if ticket_count == 0:
			print("No ticket")
	else:
		if len(ticket_number) < 6:
			print("ERROR: Invalid ticket number -- ticket number too short")
			logger.info("Invalid ticket number, going back to the control panel menu")
			return
		if not ticket_number.startswith('T'):
			print("ERROR: Invalid ticket number format -- ticket number starts with 'T'")
			logger.info("Invalid ticket number, going back to the control panel menu")
			return
		if not ticket_number[1:].isdecimal():
			print("ERROR: Invalid ticket number -- "
			      "ticket number should ba a single character 'T' followed by decimal numbers")
			logger.info("Invalid ticket number, going back to the control panel menu")
			return
		if len(ticket_number) > 6 and ticket_number[1] == '0':
			print("ERROR: Invalid ticket number -- more than 4 leading zeros")
			logger.info("Invalid ticket number, going back to the control panel menu")
			return
		if set(ticket_number[1:]) == {'0'}:
			print("ERROR: Invalid ticket number -- ticket number is all zero")
			logger.info("Invalid ticket number, going back to the control panel menu")
			return
		ticket_index: int = int(ticket_number[1:])
		ticket: Optional[Ticket] = House.searchTicket(ticket_index)
		if ticket is None:
			print("ERROR: No such ticket")
			logger.info("Invalid ticket number, going back to the control panel menu")
			return
		ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
		logger.info(f"Admin wants to check this ticket: {ticket}")
		print(f"{ticket_no:<6} @ {time} "
		      f"House {house_no:<2} -- {movie:<50} ~"
		      f"Seat <{row_index + 1}{chr(column_index + 65)}>")
	print(f"TOTAL: {House.get_n_tickets()} ticket{'s' if House.get_n_tickets() > 1 else ''} active, "
	      f"{House.total_tickets} ticket{'s' if House.total_tickets > 1 else ''} were created.")


def deleteTicket() -> None:
	"""
	Admin mode 8: Delete a ticket

	:return: None
	"""
	logger: Logger = getLogger("deleteTicket")
	logger.info("Admin Mode 8: Delete a ticket")
	logger.info("Waiting ticket number input")
	print("Please enter you ticket number (starts with 'T'):")
	ticket_number: str = input("-> ").strip().upper().replace(' ', '')
	if len(ticket_number) < 6:
		print("ERROR: Invalid ticket number -- ticket number too short")
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	if not ticket_number.startswith('T'):
		print("ERROR: Invalid ticket number format -- ticket number starts with 'T'")
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	if not ticket_number[1:].isdecimal():
		print("ERROR: Invalid ticket number -- "
		      "ticket number should ba a single character 'T' followed by decimal numbers")
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	if len(ticket_number) > 6 and ticket_number[1] == '0':
		print("ERROR: Invalid ticket number -- more than 4 leading zeros")
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	if set(ticket_number[1:]) == {'0'}:
		print("ERROR: Invalid ticket number -- ticket number is all zero")
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	ticket_index: int = int(ticket_number[1:])
	ticket: Optional[Ticket] = House.searchTicket(ticket_index)
	if ticket is None:
		print("ERROR: No such ticket")
		logger.info("Invalid ticket number, going back to the control panel menu")
		return
	ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
	logger.info(f"Admin wants to delete this ticket: {ticket}")
	print(f"{ticket_no:<6} @ {time} "
	      f"House {house_no:<2} -- {movie:<50} ~"
	      f"Seat <{row_index + 1}{chr(column_index + 65)}>")
	logger.debug(f"Ticket info: {ticket}")
	House.houses_table[house_no].seating_plan[row_index][column_index] = 0
	House.tickets_table.remove(ticket)
	print("Successfully deleted this ticket")
	logger.info(f"Ticket {ticket_no} deleted")
	saveData()
	logger.debug(f"Total: {House.get_n_tickets()} ticket{'s' if House.get_n_tickets() > 1 else ''} active")


def clearHouseSeats() -> None:
	"""
	Admin mode 9: Clear all the seats of a house

	:return: None
	"""
	logger: Logger = getLogger("clearHouseSeats")
	logger.info("Admin Mode 9: Clear all the seats of a house")
	print("House list:")
	for house in House.houses_table.values():
		if house.movie:
			print(f"House {house.house_number} now playing: {house.movie}")
		else:
			print(f"House {house.house_number} is closed")
	logger.info("Waiting house number input")
	house_num_str: str = input("Enter the house number of a house which you would like to empty:\n-> ").strip()
	if not house_num_str.isdecimal():
		logger.info("Invalid house number, going back to the control panel menu")
		print("ERROR: House number can only be decimal number")
		print("Going back to the control panel menu...")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		logger.info("Invalid house number, going back to the control panel menu")
		print('ERROR: No such house')
		print("Going back to the control panel menu...")
		return
	house: House = House.houses_table[house_num]
	print(f"House {house_num}")
	house.printSeatingPlan()
	logger.info(f"Waiting to confirm clear of all seat of House {house_num}")
	confirm: str = (input("Please confirm you would like to clear all seats and tickets of this house (y/N): ")
	                .strip().upper())
	if confirm == '' or confirm == 'N':
		logger.info("Confirmation failed")
		print("Going back to the control panel menu...")
		return
	elif confirm == 'Y':
		logger.info("Confirmed, clearing seating plan")
		print(f"Clearing all seat of house {house_num}")
		house.clearPlan()
		print("Deleting all related tickets")
		logger.info("Deleting all related tickets")
		n_tickets_removed: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_num, *other_information = ticket
			if house_num == house.house_number:
				logger.info(f"Deleting {ticket_num}, ticket info: {ticket}")
				House.tickets_table.remove(ticket)
				n_tickets_removed += 1
		print(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}")
		logger.info(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}")
		saveData()
		return
	else:
		logger.info("Confirmation failed")
		print("ERROR: Invalid confirmation")
		print("Confirmation failed")
		print("Going back to the control panel menu...")
		return


def deleteHouse() -> None:
	"""
	Admin mode 10: DELETE A HOUSE

	:return: None
	"""
	logger: Logger = getLogger('deleteHouse')
	logger.info("Admin mode 10: DELETE A HOUSE")
	print("House list:")
	house_count: int = 0
	for house in House.houses_table.values():
		if house.movie:
			print(f"House {house.house_number} now playing: {house.movie}")
		else:
			print(f"House {house.house_number} is closed")
	if house_count == 0:
		logger.info("No house, Going back to the control panel menu...")
		print("No house")
		return
	logger.info("Waiting house number input")
	house_num_str: str = input("Enter the house number of a house which you would like to delete:\n-> ").strip()
	if not house_num_str.isdecimal():
		logger.info("Invalid house number, going back to the control panel menu")
		print("ERROR: House number can only be decimal number")
		print("Going back to the control panel menu...")
		return
	house_num: int = int(house_num_str)
	if house_num not in House.houses_table.keys():
		logger.info("Invalid house number, going back to the control panel menu")
		print('ERROR: No such house')
		print("Going back to the control panel menu...")
		return
	house: House = House.houses_table[house_num]
	print(f"House {house_num}")
	house.printSeatingPlan()
	logger.info(f"Waiting to confirm clear of all seat of House {house_num}")
	confirm: str = input("Please confirm you would like to delete this house (y/N): ").strip().upper()
	if confirm == '' or confirm == 'N':
		logger.info("Confirmation failed")
		print("Going back to the control panel menu...")
		return
	elif confirm == 'Y':
		logger.info("Confirmed, clearing seating plan")
		print(f"Clearing all seat of house {house_num}")
		house.clearPlan()
		print("Deleting all related tickets")
		logger.info("Deleting all related tickets")
		n_tickets_removed: int = 0
		for ticket in House.tickets_table:
			ticket_index, ticket_num, *other_information = ticket
			if house_num == house.house_number:
				logger.info(f"Deleting {ticket_num}, ticket info: {ticket}")
				House.tickets_table.remove(ticket)
				n_tickets_removed += 1
		print(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}")
		logger.info(f"Removed {n_tickets_removed} ticket{'s' if n_tickets_removed > 1 else ''}")
		print("Removing this house")
		logger.info("Removing this house")
		del House.houses_table[house_num]
		# No need House.house_num -= 1, as it is only for giving new house number
	else:
		logger.info("Confirmation failed")
		print("ERROR: Invalid confirmation")
		print("Confirmation failed")
		print("Going back to the control panel menu...")
		return


def clearAllData() -> None:
	"""
	Admin Mode 11: CLEAR ALL DATA
	
	:return: None
	"""
	logger: Logger = getLogger("clearAllData")
	logger.info("Admin Mode 11: CLEAR ALL DATA")
	logger.info("Confirming")
	confirm: str = input("Please confirm you would like to clear ALL data (y/N): ").strip().upper()
	if confirm == '' or confirm == 'N':
		logger.info("Confirmation failed, going back to the control panel menu")
		print("Going back to the control panel menu...")
		return
	elif confirm == 'Y':
		pass
	else:
		logger.info("Confirmation failed, going back to the control panel menu")
		print("ERROR: Invalid confirmation")
		print("Confirmation failed")
		print("Going back to the control panel menu...")
		return
	House.tickets_table = []
	House.total_tickets = 0
	logger.info("Removed unsaved tickets data")
	print("Successfully removed unsaved tickets data")
	try:
		logger.info("Finding any saved tickets data")
		absolute_path = path.dirname(__file__)
		relative_path = '../../data/tickets'
		full_path = path.join(absolute_path, relative_path)
		logger.debug(f"Full path = {full_path}")
		remove(full_path)
	except FileNotFoundError:
		logger.info("No saved tickets data")
		print("No saved tickets data")
	else:
		logger.info("DELETED SAVED TICKETS DATA")
		print("Successfully deleted saved tickets data")
	finally:
		logger.info("Process of removing tickets data finished")
		print("Process of removing tickets data finished")
	House.houses_table = {}
	House.n_House = 0
	logger.info("Removed unsaved houses data")
	print("Successfully removed local houses data")
	try:
		logger.info("Finding any saved houses data")
		absolute_path = path.dirname(__file__)
		relative_path = '../../data/houses'
		full_path = path.join(absolute_path, relative_path)
		remove(full_path)
	except FileNotFoundError:
		logger.info("No saved houses data")
		print("No saved houses data")
	else:
		logger.info("DELETED SAVED HOUSES DATA")
		print("Successfully deleted saved houses data")
	finally:
		logger.info("Process of removing houses data finished")
		print("Process of removing tickets houses finished")
	print("Finish!")
	logger.info("Finished clearing all saved data!")


def changeColour() -> None:
	"""
	Admin Mode 14: Change the colour scheme
	
	:return: None
	"""
	from .colour import colour_mode
	
	logger: Logger = getLogger("changeColour")
	logger.info("Admin Mode 14: Change the colour scheme")
	if colour_mode == 'DARK':
		logger.info("The colour scheme is now DARK, changing to LIGHT...")
		setColour('LIGHT')
	elif colour_mode == 'LIGHT':
		logger.info("The colour scheme is now LIGHT, changing to DARK...")
		setColour('DARK')
	else:
		logger.info("ERROR: Unknown colour scheme, changing to DARK anyway...")
		setColour('DARK')


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
		from .colour import normal_colour
		
		logger: Logger = getLogger("adminMode")
		logger.info("Entered main menu of the Control Panel")
		print(normal_colour)
		logger.info("Waiting mode code input")
		print("\n"
		      "0: EXIT CONTROL PANEL\n"
		      "1: Create a new house\n"
		      "2: Update the movie of a house\n"
		      "3: Save data\n"
		      "4: Load data\n"
		      "5: Check houses information\n"
		      "6: Seat status override\n"
		      "7: Check ticket information\n"
		      "8: Delete a ticket\n"
		      "9: Clear all the seats of a house\n"
		      "10: DELETE A HOUSE\n"
		      "11: CLEAR ALL DATA\n"
		      "12: STOP THE ENTIRE PROGRAM\n"
		      "13: Help\n"
		      "14: Change the colour scheme"
		      )
		mode: str = input("Please choose a mode (0/1/2/3/4/5/6/7/8/9/10/11/12/13)\n-> ").strip()
		if not mode.isdecimal():
			print("ERROR: Mode code should be all decimal")
			logger.info("Invalid mode code")
			continue
		
		# EXIT CONTROL PANEL
		if mode == '0':
			print("Bye!")
			logger: Logger = getLogger("adminMode.mode_0")
			logger.info("Admin Mode 0: EXIT CONTROL PANEL")
			logger.info("ADMIN LOGOUT")
			return
		
		# Create a new house
		elif mode == '1':
			createHouse()
		
		# Update the movie of a house
		elif mode == '2':
			updateMovie()
		
		# Save data
		elif mode == '3':
			logger: Logger = getLogger("adminMode.mode_3")
			logger.info("Admin Mode 3: Save data")
			saveData(print_log=True)
		
		# Load data
		elif mode == '4':
			logger: Logger = getLogger("adminMode.mode_4")
			logger.info("Admin Mode 4: Load data")
			loadData(print_log=True)
		
		# Check houses information
		elif mode == '5':
			checkHousesInformation()
		
		# Seat status override
		elif mode == '6':
			seatStatusOverride()
		
		# Check ticket information
		elif mode == '7':
			checkTicketInformation()
		
		# Delete a ticket
		elif mode == '8':
			deleteTicket()
		
		# Clear all seats of a house
		elif mode == '9':
			clearHouseSeats()
		
		# DELETE A HOUSE
		elif mode == '10':
			deleteHouse()
		
		# CLEAR ALL DATA
		elif mode == '11':
			clearAllData()
		
		# STOP THE ENTIRE PROGRAM
		elif mode == '12':
			logger: Logger = getLogger("adminMode.mode_12")
			logger.info("QUITING PROGRAM: Admin mode 12")
			print("Bye!")
			quit()
		
		# Help
		elif mode == '13':
			logger: Logger = getLogger("adminMode.mode_13")
			logger.info("Admin Mode 13: Help")
			openWebBrowser("https://joeccp.github.io/SBA/")
			logger.info("Opened a website browser and visit https://joeccp.github.io/SBA/")
		
		# Change the colour scheme
		elif mode == '14':
			changeColour()
		
		else:
			logger.info("Unknown mode code")
			print(f"ERROR: Unknown mode code {mode}")
