"""User mode"""

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

import webbrowser
from datetime import datetime
from logging import getLogger, Logger
from string import ascii_uppercase
from time import sleep

from .colour import *
from .house import House
from .utils import clearScreen, saveData


def userMode() -> None:
	"""
	User mode
	:return: None
	"""
	message: str = ""
	while True:
		logger: Logger = getLogger("userMode")
		logger.info("Entered the user menu")
		clearScreen()
		print("CINEMA KIOSK SYSTEM\n\n\n")
		print(Colour.RED + message + normal_colour + "\n\n\n")
		for house in House.houses_table.values():
			if house.movie:
				print(
					f"House {house.house_number}: {house.movie:<50} {Colour.GREEN if house.n_available > 0 else Colour.RED}{house.n_available}{normal_colour}/{house.n_seat}")
		print(
			"\n"
			"0: LOG OUT\n"
			"1: Buy ticket\n"
			"2: Check ticket\n"
			"3: Ticket refund\n"
			"4: HELP\n"
			"Please select a mode (0/1/2/3):"
		)
		logger.info("Waiting mode code input")
		mode: str = input("-> ").strip()
		if not mode.isdecimal():
			message: str = "ERROR: Mode number should be a decimal number."
			logger.info("Invalid mode code")
			continue
		if mode == '0':
			logger: Logger = getLogger("userMode.mode_0")
			logger.info("User Mode 0: Log out")
			logger.info("USER LOGOUT")
			for i in range(3, 0, -1):
				print(f"\rYou will be logged out after {i} seconds...", end='')
				sleep(1)
			return
		
		# Buy ticket
		elif mode == '1':
			logger: Logger = getLogger("userMode.mode_1")
			logger.info("User Mode 1: Buy ticket")
			clearScreen()
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n")
			print("House(s) available:")
			total_available_house_count: int = 0
			for house in House.houses_table.values():
				if house.movie and house.n_available != 0:
					print(f"House {house.house_number}: {house.movie:<50} {house.n_available}/{house.n_seat}")
					total_available_house_count += 1
			if total_available_house_count == 0:
				message: str = "Sorry, no house available now"
				continue
			print("\nPlease enter the house number (or hit Enter to go back to the main menu):")
			logger.info("Waiting house number input")
			house_num_str: str = input("-> ").strip()
			if house_num_str == '':
				message: str = ''
				logger.info("Empty house number, going back to the user menu")
				continue
			if not house_num_str.isdecimal():
				message: str = "ERROR: House number can only be decimal numbers"
				logger.info("Invalid house number, going back to the user menu")
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.houses_table.keys():
				message: str = "ERROR: That house does not exist"
				logger.info("Invalid house number, going back to the user menu")
				continue
			house: House = House.houses_table[house_num]
			logger.info(f"User selected house {house_num}")
			clearScreen()
			print(f"House {house.house_number} is now playing: {house.movie}")
			house.printPlan()
			print(
				f"\nEnter the {row_colour}row{normal_colour} and {column_colour}column{normal_colour} number of the seat "
				f"(or just hit Enter to go back to the main menu):")
			logger.info("Waiting seat coordinate input")
			coor: str = input("\n-> ").strip().upper().replace(" ", '')
			if coor == '':
				message: str = ''
				logger.info("Empty coordinate, going back to the user menu")
				continue
			if len(coor) == 1:
				logger.info("Invalid coordinate, going back to the user menu")
				message: str = "ERROR: Invalid format of the seat number"
				continue
			if coor[-1] not in ascii_uppercase:
				logger.info("Invalid coordinate, going back to the user menu")
				message: str = f"ERROR: {column_colour}Column{normal_colour} index is not a character"
				continue
			column_str: str = coor[-1]
			column_int: int = ord(column_str) - 65
			if column_int >= house.n_column:
				logger.info("Invalid coordinate, going back to the user menu")
				message: str = f"ERROR: Invalid {column_colour}column{normal_colour}"
				continue
			row_str: str = coor[:-1]
			if len(row_str) > 2:
				logger.info("Invalid coordinate, going back to the user menu")
				message: str = f"ERROR: Impossible {row_colour}row{normal_colour} number"
				continue
			row_int: int = int(row_str) - 1
			if house.seating_plan[row_int][column_int] != 0:
				logger.info("Seat already sold, going back to the user menu")
				message: str = "Sorry, the seat is not available"
				continue
			house.seating_plan[row_int][column_int] = 1
			House.total_tickets += 1
			ticket_index: int = House.total_tickets
			ticket_number: str = f"T{ticket_index:0>5}"
			time: str = datetime.now().isoformat(timespec="seconds")
			ticket: tuple[int, str, str, int, str, int, int] = (
				ticket_index, ticket_number, time, house.house_number, house.movie, row_int, column_int
			)
			print("Your ticket:")
			print(f"{ticket_number:<6} @ {time}: "
			      f"House {house.house_number:<2} -- {house.movie:<50} ~"
			      f"Seat <{row_colour}{row_int + 1}{column_colour}{chr(column_int + 65)}{normal_colour}>")
			logger.info("User has successfully bought a ticket")
			logger.info(f"Ticket info: {ticket}")
			House.tickets_table.append(ticket)
			saveData()
			print("\n\nThank you for your purchase!")
			input("\nHit Enter to go back to the main menu")
			message: str = ""
			continue
		
		
		# Check ticket
		elif mode == '2':
			logger: Logger = getLogger("userMode.mode_2")
			logger.info("User Mode 2: Check ticket")
			clearScreen()
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n")
			print("Please enter you ticket number (starts with 'T'):")
			logger.info("Waiting ticket number input")
			ticket_number: str = input("-> ").strip().upper()
			if ticket_number == "":
				message: str = ""
				logger.info("Empty ticket number, going back to the user menu")
				continue
			if not ticket_number.startswith('T'):
				message: str = "ERROR: Invalid ticket number format -- ticket number starts with 'T'"
				logger.info("Invalid ticket number, going back to the user menu")
				continue
			if ticket_number == 'T':
				message: str = "ERROR: Invalid ticket number -- ticket number has no decimal numbers"
				logger.info("Invalid ticket number, going back to the user menu")
				continue
			if len(ticket_number) < 6:
				message: str = "ERROR: Invalid ticket number -- ticket number too short"
				logger.info("Invalid ticket number, going back to the user menu")
				continue
			if not ticket_number[1:].isdecimal():
				message: str = ("ERROR: Invalid ticket number -- "
				                "ticket number should ba a single character 'T' followed by decimal numbers")
				logger.info("Invalid ticket number, going back to the user menu")
				continue
			if len(ticket_number) > 6 and ticket_number[1] == '0':
				message: str = "ERROR: Invalid ticket number -- more than 4 leading zeros"
				logger.info("Invalid ticket number, going back to the control panel menu")
				continue
			if set(ticket_number[1:]) == {'0'}:
				message: str = "ERROR: Invalid ticket number -- ticket number is all zero"
				logger.info("Invalid ticket number, going back to the control panel menu")
				continue
			print()
			ticket_index: int = int(ticket_number[1:])
			ticket = House.searchTicket(ticket_index)
			if ticket is None:
				logger.info("No such ticket, going back to the user menu")
				print("No such ticket")
				print("\n\n")
				input("Hit enter to go back to the main menu")
				message: str = ""
				continue
			ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
			print(f"{ticket_no:<6} @ {time} "
			      f"House {house_no:<2} -- {movie:<30} ~ "
			      f"Seat <{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}>")
			print("\n\n")
			input("Hit enter to go back to the main menu")
			message: str = ""
		
		# Ticket refund
		elif mode == '3':
			logger: Logger = getLogger("userMode.mode_3")
			logger.info("User Mode 3: Ticket refund")
			clearScreen()
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n\n\n\n\n\n")
			print("Please enter you ticket number (starts with 'T'):")
			logger.info("Waiting ticket number input")
			ticket_number: str = input("-> ").strip().upper().replace(' ', '')
			if ticket_number == "":
				logger.info("Empty ticket number, going back to the user menu")
				message: str = ""
				continue
			if not ticket_number.startswith('T'):
				logger.info("Invalid ticket number, going back to the user menu")
				message: str = "ERROR: Invalid ticket number format -- ticket number starts with 'T'"
				continue
			if ticket_number == 'T':
				logger.info("Invalid ticket number, going back to the user menu")
				message: str = "ERROR: Invalid ticket number -- ticket number has no decimal numbers"
				continue
			if len(ticket_number) < 6:
				logger.info("Invalid ticket number, going back to the user menu")
				message: str = "ERROR: Invalid ticket number -- ticket number too short"
				continue
			if not ticket_number[1:].isdecimal():
				logger.info("Invalid ticket number, going back to the user menu")
				message: str = ("ERROR: Invalid ticket number -- "
				                "ticket number should ba a single character 'T' followed by decimal numbers")
				continue
			if len(ticket_number) > 6 and ticket_number[1] == '0':
				message: str = "ERROR: Invalid ticket number -- more than 4 leading zeros"
				logger.info("Invalid ticket number, going back to the control panel menu")
				continue
			if set(ticket_number[1:]) == {'0'}:
				message: str = "ERROR: Invalid ticket number -- ticket number is all zero"
				logger.info("Invalid ticket number, going back to the control panel menu")
				continue
			print()
			ticket_index: int = int(ticket_number[1:])
			ticket = House.searchTicket(ticket_index)
			if ticket is None:
				logger.info("No such ticket, going back to the user menu")
				print("No such ticket")
				print("\n\n")
				input("Hit enter to go back to the main menu")
				message: str = "ERROR: No such ticket"
				continue
			ticket_index, ticket_no, time, house_no, movie, row_index, column_index = ticket
			logger.info(f"User want to delete this ticket: {ticket}")
			print(f"{ticket_no:<6} @ {time} "
			      f"House {house_no:<2} -- {movie:<50} ~"
			      f"Seat <{row_colour}{row_index + 1}{column_colour}{chr(column_index + 65)}{normal_colour}>")
			print("\nAre you sure you want to get refund of this ticket? (y/N)")
			logger.info("Confirming")
			confirm: str = input("-> ").strip().upper()
			if confirm == 'Y':
				House.houses_table[house_no].seating_plan[row_index][column_index] = 0
				House.tickets_table.remove(ticket)
				logger.info("Ticket deleted")
				saveData()
				print("\nRefund succeed!")
				message: str = ''
				continue
			else:
				logger.info("Confirmation failed, go back to the user menu")
				print()
				message: str = "ERROR: Confirmation failed. Refund Failed"
				continue
			
		
		# HELP
		elif mode == '4':
			logger: Logger = getLogger("userMode.mode_4")
			logger.info("User Mode 4: Help")
			webbrowser.open("https://joeccp.github.io/SBA/")
			logger.info("Opened a website browser and visit https://joeccp.github.io/SBA/")
		
		else:
			logger.info("Unknown mode code")
			message: str = "ERROR: Unknown mode"
			continue
