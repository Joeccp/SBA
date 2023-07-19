"""Common constants, functions and classes"""
from os import get_terminal_size
import string

terminal_width, terminal_height = tuple(get_terminal_size())


def charToDigit(char: str) -> int:
	"""
	Translate a single alphabet character to a digit (starts from 0) which represent the order of the character
	
	>>> charToDigit("A")
	0
	>>> charToDigit("B")
	1
	>>> charToDigit("Z")
	25
	
	:param char: Single character A-Z (case-insensitive) (one-character string)
	:type char: str
	:return: Digit (starts from 0) which represent the order of the character
	:rtype: int
	:exception TypeError: If parameter `char` is not a string
	:exception ValueError: If parameter `char` is invalid
	"""
	if type(char) is not str:
		err_msg: str = f"`char` must be a string, not {type(char).__name__}"
		raise TypeError(err_msg)
	if char == "":
		err_msg: str = f"`char` must be a single alphabet character, not an empty string"
		raise ValueError(err_msg)
	if len(char) > 1:
		err_msg: str = (f"`char` must be a single alphabet character (one-character string), "
		                "not a string with multiple characters")
		raise ValueError(err_msg)
	char: str = char.upper()
	if char not in string.ascii_uppercase:  # if char not in A-Z:
		err_msg: str = f"`char` must be a single alphabet character (A-Z)"
		raise ValueError(err_msg)
	ret: int = ord(char) - 65
	return ret
	


def alphabetToColumnIndex(alphabet: str) -> int:
	"""
	Translate alphabet index of a column to a seating plan column index (integer which starts from 0)
	
	A -> 0
	B -> 1
	C -> 2
	...
	Z -> 25
	AA -> 26
	AB -> 27
	
	It is somehow similar to a base26 to base10 convertor.
	
	:param alphabet: Alphabet index of a column
	:type alphabet: str
	:return: Seating plan column index
	:rtype: int
	"""


def seatIDtoPlanIndex(seatID: str) -> tuple[int, int]:
	...
