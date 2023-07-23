"""User mode"""
from house import House
from common import clearScreen
from time import sleep
from datetime import datetime


def userMode():
	message: str = ""
	while True:
		clearScreen()
		print("CINEMA KIOSK SYSTEM\n\n\n")
		print(message + "\n\n\n")
		for house in House.table.values():
			if house.movie:
				print(f"House {house.house_number}: {house.movie:<50} {house.available}/{house.n_seat}")
		print(
			"\n"
			"0: LOG OUT"
			"1: Buy ticket"
			"2: Check ticket"
			"3: Refund"
			"Please select a mode (0/1/2/3):"
		)
		mode: str = input("-> ").strip()
		if not mode.isdecimal():
			message: str = "ERROR: Mode number should be a decimal number."
			continue
		if mode == '0':
			print("You will be logged out after 3 seconds...")
			sleep(3)
			return
		
		elif mode == '1':
			clearScreen()
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n")
			print("House(s) available:")
			for house in House.table.values():
				if house.movie and house.available != 0:
					print(f"House {house.house_number}: {house.movie:<50} {house.available}/{house.n_seat}")
			print("\nPlease enter the house number (or hit Enter to go back to the main menu):")
			house_num_str: str = input("-> ").strip()
			if house_num_str == '':
				message: str = ''
				continue
			if not house_num_str.isdecimal():
				...
			
			
		
		elif mode == '2':
			clearScreen()
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n")
			print("Please enter you ticket number (starts with 'T'):")
			ticket_number: str = input("-> ").strip().upper()
			if len(ticket_number) < 6:
				message: str = "ERROR: Invalid ticket number -- ticket number too short"
				continue
			if not ticket_number.startswith('T'):
				message: str = "ERROR: Invalid ticket number format -- ticket number starts with 'T'"
				continue
			if not ticket_number[1:].isdecimal():
				message: str = ("ERROR: Invalid ticket number -- "
				                "ticket number should ba a single character 'T' followed by decimal numbers")
				continue
			print()
			for ticket in House.tickets:
				if ticket[0] == ticket_number:
					ticket_no, time, house_no, movie, row_index, column_index = ticket
					print(f"{ticket_no:<6} @ {time}: "
					      f"House {house_no:<2} -- {movie:<50} ~"
					      f"Seat <{row_index + 1}{chr(column_index + 65)}>")
					print("\n\n")
					input("Hit enter to go back to the main menu")
					message: str = ""
					break
					
			else:
				print("No such ticket")
				print("\n\n")
				input("Hit enter to go back to the main menu")
				message: str = ""
				
			continue
			
		elif mode == '3':
			clearScreen()
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n")
			print("Please enter you ticket number (starts with 'T'):")
			ticket_number: str = input("-> ").strip().upper()
			if len(ticket_number) < 6:
				message: str = "ERROR: Invalid ticket number -- ticket number too short"
				continue
			if not ticket_number.startswith('T'):
				message: str = "ERROR: Invalid ticket number format -- ticket number starts with 'T'"
				continue
			if not ticket_number[1:].isdecimal():
				message: str = ("ERROR: Invalid ticket number -- "
				                "ticket number should ba a single character 'T' followed by decimal numbers")
				continue
			print()
			for ticket in House.tickets:
				if ticket[0] == ticket_number:
					ticket_no, time, house_no, movie, row_index, column_index = ticket
					print(f"{ticket_no:<6} @ {time}: "
					      f"House {house_no:<2} -- {movie:<50} ~"
					      f"Seat <{row_index + 1}{chr(column_index + 65)}>")
					print("\nAre you sure you want to get refund of this ticket? (y/N)")
					confirm: str = input("-> ").strip().upper()
					if confirm == 'Y':
						House.tickets.remove(ticket)
						print("\nRefund succeed!")
					else:
						print()
						message: str = "ERROR: Confirmation failed. Refund Failed"
						break
			
			else:
				print("No such ticket")
				print("\n\n")
				input("Hit enter to go back to the main menu")
				message: str = ""
			
			continue
			
			
		else:
			message: str = "ERROR: Unknown mode"
			continue
			
			