"""User mode"""
from house import House
from common import clearScreen
from time import sleep
from datetime import datetime
from string import ascii_uppercase


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
			"0: LOG OUT\n"
			"1: Buy ticket\n"
			"2: Check ticket\n"
			"3: Refund\n"
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
			total_available_house_count: int = 0
			for house in House.table.values():
				if house.movie and house.available != 0:
					print(f"House {house.house_number}: {house.movie:<50} {house.available}/{house.n_seat}")
					total_available_house_count += 1
			if total_available_house_count == 0:
				message: str = "Sorry, no house available now"
				continue
			print("\nPlease enter the house number (or hit Enter to go back to the main menu):")
			house_num_str: str = input("-> ").strip()
			if house_num_str == '':
				message: str = ''
				continue
			if not house_num_str.isdecimal():
				message: str = "ERROR: House number can only be decimal numbers"
				continue
			house_num: int = int(house_num_str)
			if house_num not in House.table.keys():
				message: str = "ERROR: That house does not exist"
				continue
			house: House = House.table[house_num]
			clearScreen()
			print(f"House {house.house_number} is now playing: {house.movie}")
			house.printPlan()
			print("\nEnter the row and column number of the seat (or just hit Enter to go back to the main menu):")
			coor: str = input("\n-> ").strip().upper().replace(" ", '')
			if coor == '':
				message: str = ''
				continue
			if coor[-1] not in ascii_uppercase:
				message: str = "ERROR: Column index is not a character"
				continue
			column_str: str = coor[-1]
			column_int: int = ord(column_str) - 65
			if column_int >= house.n_column:
				message: str = "ERROR: Invalid column"
				continue
			row_str: str = coor[:-1]
			if len(row_str) > 2:
				message: str = "ERROR: Impossible row number"
				continue
			row_int: int = int(row_str) - 1
			if house.plan[row_int][column_int] != 0:
				message: str = "Sorry, the seat is not available"
				continue
			house.plan[row_int][column_int] = 1
			ticket_number: str = f"T{House.n_tickets+1:0>5}"
			time: str = datetime.now().isoformat()
			ticket: tuple[str, str, int, str, int, int] = (
				ticket_number, time, house.house_number, house.movie, row_int, column_int
			)
			print("Your ticket:")
			print(f"{ticket_number:<6} @ {time}: "
			      f"House {house.house_number:<2} -- {house.movie:<50} ~"
			      f"Seat <{row_int + 1}{chr(column_int + 65)}>")
			House.tickets.append(ticket)
			print("\n\nThank you for your purchase!")
			input("\nHit Enter to go back to the main menu")
			message: str = ""
			continue
			
			
		
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
			print("CINEMA KIOSK SYSTEM\n\n\n\n\n\n\n\n\n\n\n\n")
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
			


if __name__ == '__main__':
    userMode()