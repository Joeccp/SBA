"""Defines different colour code"""


class Colour:
	RESET: str = '\033[0m'
	BLUE: str = '\033[1;94m'  # For row letters
	PURPLE: str = '\033[1;35m'  # For column numbers
	RED: str = '\033[1;31m'
	BLACK: str = '\033[30m'
	GREEN: str = '\033[1;32m'
	WHITE_BG: str = '\033[47m'
	GREEN_BG: str = '\033[102m'
	YELLOW_BG: str = '\033[103m'
	RED_BG: str = '\033[101m'




row_colour: str = Colour.BLUE
column_colour: str = Colour.PURPLE
# normal_colour: str = Colour.WHITE_BG + Colour.BLACK
normal_colour: str = '\033[30;47m'
