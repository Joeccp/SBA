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
		      "6: Buy / Reserve / Empty a seat"
		      )
		mode: str = input("Please enter the action you want to perform (0/1/2/3/4/5/6)\n-> ").strip()
		if not mode.isdecimal():
			print("ERROR: Action code should be all decimal")
			continue
		if mode not in ('0', '1', '2', '3', '4', '5', '6'):
			print("ERROR: Unknown Action code")
			continue
		if mode == '0':
			print('Bye!')
			return
		
		# Create house
		elif mode == '1':
			print(f"House {House.n_House + 1} will be the new house")
			n_row_str: str = input(f"Enter how many row does {House.n_House + 1} has (1-99): ").strip()
			if not n_row_str.isdecimal():
				print("ERROR: Number of rows must be decimal number")
				print("House creation failed, exiting to control panel menu...")
				continue
			n_row: int = int(n_row_str)
			if n_row > 99:
				print("Unsupported large number of rows")
				print("House creation failed, exiting to control panel menu...")
				continue
			n_col_str: str = input(f"Enter how many column does {House.n_House + 1} has (1-26): ").strip()
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
			house_num_str: str = input("Please select the house:\n->").strip()
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
			
					
					
					
					
					
					
					
					
if __name__ == '__main__':
    adminMode()