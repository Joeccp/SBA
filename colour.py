"""Defines different colour code"""


class Colour:
	RESET: str = '\033[0m'
	BLUE: str = '\033[94m'  # For row letters
	PURPLE: str = '\033[35m'  # For column numbers
	WHITE_BG: str = '\033[47m'
	BLACK: str = '\033[30m'
	
	



row_colour: str = Colour.BLUE
column_colour: str = Colour.PURPLE
normal: str = Colour.WHITE_BG + Colour.BLACK

if __name__ == '__main__':
	print(normal, "NORMAL")
	print(row_colour, "ROW NUMBER")
	print(column_colour, "COLUMN NUMBER")